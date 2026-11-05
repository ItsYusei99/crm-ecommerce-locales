from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from .auth import login_requerido, rol_requerido
from .db import get_db
from .servicios import (RESULTADOS, TIPOS_CONTACTO, link_whatsapp, patron_like, plantillas_de,
                        registrar_actividad, render_plantilla)

bp = Blueprint("clientes", __name__, url_prefix="/clientes")
POR_PAGINA = 25


@bp.route("/")
@login_requerido
def lista():
    q = request.args.get("q", "").strip()
    seg = request.args.get("segmento", "")
    try:
        pagina = max(1, int(request.args.get("pagina", 1)))
    except ValueError:
        pagina = 1
    where, params = " WHERE 1=1", []
    if q:
        where += " AND (nombre LIKE ? ESCAPE '\\' OR telefono_wa LIKE ? ESCAPE '\\' OR ig_user LIKE ? ESCAPE '\\')"
        params += [patron_like(q)] * 3
    if seg:
        where += " AND segmento=?"
        params.append(seg)
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM Cliente" + where, params).fetchone()[0]
    clientes = db.execute(
        "SELECT * FROM Cliente" + where + " ORDER BY ltv DESC, id_cliente LIMIT ? OFFSET ?",
        params + [POR_PAGINA, (pagina - 1) * POR_PAGINA]).fetchall()
    paginas = max(1, -(-total // POR_PAGINA))
    return render_template("clientes/lista.html", clientes=clientes, q=q, segmento=seg,
                           pagina=pagina, paginas=paginas, total=total)


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
    links = {k: link_whatsapp(c["telefono_wa"], render_plantilla(v, c["nombre"].split()[0]))
             for k, v in plantillas_de(db).items()}
    return render_template("clientes/ficha.html", c=c, pedidos=pedidos, contactos=contactos, links=links)


@bp.route("/<int:id_cliente>/editar", methods=("GET", "POST"))
@login_requerido
def editar(id_cliente):
    c = _obtener(id_cliente)
    if request.method == "POST":
        datos = _form_cliente()
        if not datos[0] or not datos[1].isdigit():
            flash("Nombre obligatorio y telefono solo con numeros.")
        else:
            db = get_db()
            try:
                db.execute("UPDATE Cliente SET nombre=?, telefono_wa=?, ig_user=?, email=? WHERE id_cliente=?",
                           (*datos, id_cliente))
            except db.IntegrityError:
                flash("Ya existe un cliente con ese WhatsApp.")
            else:
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
    mensaje = request.form.get("mensaje", "").strip()
    resultado = request.form.get("resultado", "pendiente")
    if request.form.get("tipo") not in TIPOS_CONTACTO or resultado not in RESULTADOS or not mensaje:
        flash("Contacto invalido: revisa tipo, resultado y mensaje.")
        return redirect(url_for("clientes.ficha", id_cliente=id_cliente))
    db = get_db()
    db.execute("INSERT INTO Interaccion (id_cliente, tipo, mensaje, resultado) VALUES (?,?,?,?)",
               (id_cliente, request.form["tipo"], mensaje, resultado))
    registrar_actividad(db, "contacto", f"{request.form['tipo']} con {c['nombre']}")
    db.commit()
    return redirect(url_for("clientes.ficha", id_cliente=id_cliente))
