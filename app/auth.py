import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .servicios import registrar_actividad

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def cargar_usuario():
    uid = session.get("uid")
    g.usuario = get_db().execute("SELECT * FROM Usuario WHERE id_usuario=?", (uid,)).fetchone() if uid else None


def login_requerido(vista):
    @functools.wraps(vista)
    def envoltura(**kw):
        if g.usuario is None:
            return redirect(url_for("auth.login"))
        return vista(**kw)
    return envoltura


def rol_requerido(*roles):
    def decorador(vista):
        @functools.wraps(vista)
        @login_requerido
        def envoltura(**kw):
            if g.usuario["rol"] not in roles:
                abort(403)
            return vista(**kw)
        return envoltura
    return decorador


@bp.route("/registro", methods=("GET", "POST"))
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        correo = request.form["correo"].strip().lower()
        password = request.form["password"]
        error = None
        if not nombre or not correo:
            error = "Nombre y correo son obligatorios."
        elif len(password) < 8:
            error = "La contrasena debe tener al menos 8 caracteres."
        if error is None:
            db = get_db()
            # El primer usuario del sistema queda como admin; los demas como colaborador.
            rol = "admin" if db.execute("SELECT COUNT(*) FROM Usuario").fetchone()[0] == 0 else "colaborador"
            try:
                db.execute("INSERT INTO Usuario (nombre, correo, password_hash, rol) VALUES (?,?,?,?)",
                           (nombre, correo, generate_password_hash(password), rol))
                db.commit()
            except db.IntegrityError:
                error = "Ese correo ya esta registrado."
            else:
                flash("Cuenta creada, ya puedes iniciar sesion.")
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/registro.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        db = get_db()
        u = db.execute("SELECT * FROM Usuario WHERE correo=?",
                       (request.form["correo"].strip().lower(),)).fetchone()
        if u is None or not check_password_hash(u["password_hash"], request.form["password"]):
            flash("Correo o contrasena incorrectos.")
        else:
            session.clear()
            session["uid"] = u["id_usuario"]
            g.usuario = u
            registrar_actividad(db, "login", u["correo"])
            db.commit()
            return redirect(url_for("index"))
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/usuarios", methods=("GET", "POST"))
@rol_requerido("admin")
def usuarios():
    db = get_db()
    if request.method == "POST":
        db.execute("UPDATE Usuario SET rol=? WHERE id_usuario=?", (request.form["rol"], request.form["id_usuario"]))
        registrar_actividad(db, "cambio_rol", f"usuario {request.form['id_usuario']} -> {request.form['rol']}")
        db.commit()
    lista = db.execute("SELECT id_usuario, nombre, correo, rol FROM Usuario ORDER BY id_usuario").fetchall()
    return render_template("auth/usuarios.html", usuarios=lista)
