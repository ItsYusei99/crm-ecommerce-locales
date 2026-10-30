"""Reglas de negocio compartidas: LTV, segmentacion y bitacora."""
from datetime import datetime, timedelta
from flask import g

PLANTILLAS = {
    "gracias": "Hola {nombre}, gracias por tu compra. Cualquier duda aqui estamos.",
    "reactivar": "Hola {nombre}, hace tiempo no te vemos. Tenemos novedades que te pueden gustar.",
    "resena": "Hola {nombre}, nos ayudarias mucho con una resena de tu ultimo pedido.",
}


def segmento_para(num_pedidos, ultima_compra):
    if num_pedidos == 0:
        return "nuevo"
    if ultima_compra and datetime.fromisoformat(ultima_compra) < datetime.now() - timedelta(days=30):
        return "inactivo"
    return "frecuente" if num_pedidos >= 2 else "nuevo"


def recalcular_cliente(db, id_cliente):
    r = db.execute(
        "SELECT COUNT(*) n, COALESCE(SUM(total),0) ltv, MAX(fecha) ultima FROM Pedido "
        "WHERE id_cliente=? AND estado != 'cancelado'", (id_cliente,)).fetchone()
    db.execute("UPDATE Cliente SET ltv=?, segmento=? WHERE id_cliente=?",
               (r["ltv"], segmento_para(r["n"], r["ultima"]), id_cliente))


def registrar_actividad(db, accion, detalle=""):
    usuario = g.get("usuario")
    db.execute("INSERT INTO Actividad (id_usuario, accion, detalle) VALUES (?,?,?)",
               (usuario["id_usuario"] if usuario else None, accion, detalle))


def link_whatsapp(telefono, texto):
    from urllib.parse import quote
    return f"https://wa.me/{telefono}?text={quote(texto)}"
