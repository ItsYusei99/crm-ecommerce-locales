from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from .auth import login_requerido, rol_requerido
from .db import get_db
from .servicios import registrar_actividad

bp = Blueprint("productos", __name__, url_prefix="/productos")


def _form():
    f = request.form
    nombre, tipo = f.get("nombre", "").strip(), f.get("tipo", "")
    try:
        precio = float(f.get("precio", ""))
    except ValueError:
        precio = -1
    if not nombre or tipo not in ("fisico", "digital") or precio < 0:
        return None
    return nombre, tipo, round(precio, 2)


@bp.route("/")
@login_requerido
def lista():
    productos = get_db().execute("SELECT * FROM Producto ORDER BY activo DESC, nombre").fetchall()
    return render_template("productos/lista.html", productos=productos)


@bp.route("/nuevo", methods=("GET", "POST"))
@rol_requerido("admin", "editor")
def nuevo():
    if request.method == "POST":
        datos = _form()
        if datos is None:
            flash("Nombre, tipo (fisico/digital) y precio mayor o igual a 0 son obligatorios.")
        else:
            db = get_db()
            db.execute("INSERT INTO Producto (nombre, tipo, precio) VALUES (?,?,?)", datos)
            registrar_actividad(db, "alta_producto", datos[0])
            db.commit()
            return redirect(url_for("productos.lista"))
    return render_template("productos/form.html", producto=None)


def _obtener(id_producto):
    p = get_db().execute("SELECT * FROM Producto WHERE id_producto=?", (id_producto,)).fetchone()
    if p is None:
        abort(404)
    return p


@bp.route("/<int:id_producto>/editar", methods=("GET", "POST"))
@rol_requerido("admin", "editor")
def editar(id_producto):
    p = _obtener(id_producto)
    if request.method == "POST":
        datos = _form()
        if datos is None:
            flash("Nombre, tipo (fisico/digital) y precio mayor o igual a 0 son obligatorios.")
        else:
            db = get_db()
            db.execute("UPDATE Producto SET nombre=?, tipo=?, precio=? WHERE id_producto=?", (*datos, id_producto))
            registrar_actividad(db, "edicion_producto", datos[0])
            db.commit()
            return redirect(url_for("productos.lista"))
    return render_template("productos/form.html", producto=p)


@bp.route("/<int:id_producto>/activo", methods=("POST",))
@rol_requerido("admin", "editor")
def alternar(id_producto):
    """Baja logica: el producto deja de ofrecerse pero conserva el historial de ventas."""
    p = _obtener(id_producto)
    db = get_db()
    db.execute("UPDATE Producto SET activo=? WHERE id_producto=?", (0 if p["activo"] else 1, id_producto))
    registrar_actividad(db, "baja_producto" if p["activo"] else "alta_producto", p["nombre"])
    db.commit()
    return redirect(url_for("productos.lista"))
