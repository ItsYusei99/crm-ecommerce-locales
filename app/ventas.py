from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from .auth import login_requerido
from .db import get_db
from .servicios import recalcular_cliente, registrar_actividad

bp = Blueprint("ventas", __name__, url_prefix="/ventas")
ESTADOS = ["nuevo", "pagado", "enviado", "entregado", "cancelado"]


@bp.route("/")
@login_requerido
def lista():
    db = get_db()
    pedidos = db.execute(
        "SELECT p.*, c.nombre cliente FROM Pedido p JOIN Cliente c USING(id_cliente) ORDER BY p.fecha DESC").fetchall()
    pipeline = {e: [p for p in pedidos if p["estado"] == e] for e in ESTADOS}
    return render_template("ventas/lista.html", pipeline=pipeline, estados=ESTADOS)


@bp.route("/nuevo", methods=("GET", "POST"))
@login_requerido
def nuevo():
    db = get_db()
    if request.method == "POST":
        id_cliente = int(request.form["id_cliente"])
        id_producto = int(request.form["id_producto"])
        cantidad = int(request.form.get("cantidad", 1))
        prod = db.execute("SELECT * FROM Producto WHERE id_producto=?", (id_producto,)).fetchone()
        if prod is None or cantidad < 1:
            flash("Producto o cantidad invalidos.")
        else:
            cur = db.execute(
                "INSERT INTO Pedido (id_cliente, canal, total, id_usuario_registra) VALUES (?,?,?,?)",
                (id_cliente, request.form["canal"], prod["precio"] * cantidad, g.usuario["id_usuario"]))
            db.execute("INSERT INTO DetallePedido (id_pedido, id_producto, cantidad, precio_unit) VALUES (?,?,?,?)",
                       (cur.lastrowid, id_producto, cantidad, prod["precio"]))
            recalcular_cliente(db, id_cliente)
            registrar_actividad(db, "venta", f"pedido {cur.lastrowid} por {prod['precio'] * cantidad:.2f}")
            db.commit()
            return redirect(url_for("ventas.lista"))
    clientes = db.execute("SELECT id_cliente, nombre FROM Cliente ORDER BY nombre").fetchall()
    productos = db.execute("SELECT * FROM Producto ORDER BY nombre").fetchall()
    return render_template("ventas/form.html", clientes=clientes, productos=productos)


@bp.route("/<int:id_pedido>/estado", methods=("POST",))
@login_requerido
def cambiar_estado(id_pedido):
    estado = request.form["estado"]
    if estado not in ESTADOS:
        flash("Estado invalido.")
        return redirect(url_for("ventas.lista"))
    db = get_db()
    p = db.execute("SELECT id_cliente FROM Pedido WHERE id_pedido=?", (id_pedido,)).fetchone()
    db.execute("UPDATE Pedido SET estado=? WHERE id_pedido=?", (estado, id_pedido))
    recalcular_cliente(db, p["id_cliente"])
    registrar_actividad(db, "seguimiento_venta", f"pedido {id_pedido} -> {estado}")
    db.commit()
    return redirect(url_for("ventas.lista"))
