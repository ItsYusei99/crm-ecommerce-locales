from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from .auth import login_requerido, rol_requerido
from .db import get_db
from .servicios import PLANTILLAS, link_whatsapp, registrar_actividad

bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@bp.route("/")
@login_requerido
def lista():
    q = request.args.get("q", "").strip()
    seg = request.args.get("segmento", "")
    sql, params = "SELECT * FROM Cliente WHERE 1=1", []
    if q:
        sql += " AND (nombre LIKE ? OR telefono_wa LIKE ? OR ig_user LIKE ?)"
        params += [f"%{q}%"] * 3
    if seg:
        sql += " AND segmento=?"
        params.append(seg)
    clientes = get_db().execute(sql + " ORDER BY ltv DESC", params).fetchall()
    return render_template("clientes/lista.html", clientes=clientes, q=q, segmento=seg)


def _form_cliente():
    f = request.form
    return (f["nombre"].strip(), f["telefono_wa"].strip(), f.get("ig_user", "").strip(), f.get("email", "").strip())


@bp.route("/nuevo", methods=("GET", "POST"))
@login_requerido
def nuevo():
    if request.method == "POST":
        datos = _form_cliente()
        if not datos[0] or not datos[1].isdigit():
            flash("Nombre obligatorio y telefono solo con numeros.")
        else:
            db = get_db()
            try:
                db.execute("INSERT INTO Cliente (nombre, telefono_wa, ig_user, email) VALUES (?,?,?,?)", datos)
                registrar_actividad(db, "alta_cliente", datos[0])
                db.commit()
                return redirect(url_for("clientes.lista"))
            except db.IntegrityError:
                flash("Ya existe un cliente con ese WhatsApp.")
    return render_template("clientes/form.html", cliente=None)


def _obtener(id_cliente):
    c = get_db().execute("SELECT * FROM Cliente WHERE id_cliente=?", (id_cliente,)).fetchone()
    if c is None:
        abort(404)
    return c


@bp.route("/<int:id_cliente>")
@login_requerido
def ficha(id_cliente):
    db = get_db()
    c = _obtener(id_cliente)
    pedidos = db.execute("SELECT * FROM Pedido WHERE id_cliente=? ORDER BY fecha DESC", (id_cliente,)).fetchall()
    contactos = db.execute("SELECT * FROM Interaccion WHERE id_cliente=? ORDER BY fecha DESC", (id_cliente,)).fetchall()
    links = {k: link_whatsapp(c["telefono_wa"], v.format(nombre=c["nombre"].split()[0])) for k, v in PLANTILLAS.items()}
    return render_template("clientes/ficha.html", c=c, pedidos=pedidos, contactos=contactos, links=links)


@bp.route("/<int:id_cliente>/editar", methods=("GET", "POST"))
@login_requerido
def editar(id_cliente):
    c = _obtener(id_cliente)
    if request.method == "POST":
        db = get_db()
        db.execute("UPDATE Cliente SET nombre=?, telefono_wa=?, ig_user=?, email=? WHERE id_cliente=?",
                   (*_form_cliente(), id_cliente))
        registrar_actividad(db, "edicion_cliente", c["nombre"])
        db.commit()
        return redirect(url_for("clientes.ficha", id_cliente=id_cliente))
    return render_template("clientes/form.html", cliente=c)


@bp.route("/<int:id_cliente>/eliminar", methods=("POST",))
@rol_requerido("admin")
def eliminar(id_cliente):
    db = get_db()
    c = _obtener(id_cliente)
    if db.execute("SELECT COUNT(*) FROM Pedido WHERE id_cliente=?", (id_cliente,)).fetchone()[0]:
        flash("No se puede borrar un cliente con pedidos.")
        return redirect(url_for("clientes.ficha", id_cliente=id_cliente))
    db.execute("DELETE FROM Interaccion WHERE id_cliente=?", (id_cliente,))
    db.execute("DELETE FROM Cliente WHERE id_cliente=?", (id_cliente,))
    registrar_actividad(db, "baja_cliente", c["nombre"])
    db.commit()
    return redirect(url_for("clientes.lista"))


@bp.route("/<int:id_cliente>/contacto", methods=("POST",))
@login_requerido
def contacto(id_cliente):
    """Gestion de contactos: registra una interaccion (WhatsApp, llamada, DM de Instagram)."""
    c = _obtener(id_cliente)
    db = get_db()
    db.execute("INSERT INTO Interaccion (id_cliente, tipo, mensaje, resultado) VALUES (?,?,?,?)",
               (id_cliente, request.form["tipo"], request.form["mensaje"], request.form.get("resultado", "pendiente")))
    registrar_actividad(db, "contacto", f"{request.form['tipo']} con {c['nombre']}")
    db.commit()
    return redirect(url_for("clientes.ficha", id_cliente=id_cliente))
