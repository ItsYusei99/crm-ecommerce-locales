import sqlite3
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(con_datos=True):
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    if con_datos:
        cargar_datos_prueba(db)
    db.commit()


def cargar_datos_prueba(db):
    db.executemany(
        "INSERT INTO Usuario (nombre, correo, password_hash, rol) VALUES (?,?,?,?)",
        [("Youssef", "youssef@crm.local", generate_password_hash("demo1234"), "admin"),
         ("Emmanuel", "emma@crm.local", generate_password_hash("demo1234"), "editor")])
    db.executemany(
        "INSERT INTO Cliente (nombre, telefono_wa, ig_user, email, fecha_alta) VALUES (?,?,?,?,?)",
        [("Ana Lopez", "5215512345678", "@ana.tienda", "ana@mail.com", "2026-01-10"),
         ("Luis Perez", "5215587654321", "@luis.mx", "luis@mail.com", "2026-02-01"),
         ("Maria Ruiz", "5215545678901", "@maria.ruiz", "maria@mail.com", "2025-11-20")])
    db.executemany("INSERT INTO Producto (nombre, tipo, precio) VALUES (?,?,?)",
                   [("Playera local", "fisico", 299), ("Curso marketing digital", "digital", 499)])
    db.executemany(
        "INSERT INTO Pedido (id_cliente, canal, fecha, total, estado, id_usuario_registra) VALUES (?,?,?,?,?,?)",
        [(1, "WA", "2026-08-01 10:00:00", 598, "entregado", 1),
         (1, "IG", "2026-10-20 12:00:00", 299, "pagado", 2),
         (3, "WEB", "2026-05-01 09:00:00", 499, "entregado", 1)])
    db.executemany("INSERT INTO DetallePedido (id_pedido, id_producto, cantidad, precio_unit) VALUES (?,?,?,?)",
                   [(1, 1, 2, 299), (2, 1, 1, 299), (3, 2, 1, 499)])
    db.executemany("INSERT INTO Interaccion (id_cliente, tipo, mensaje, resultado) VALUES (?,?,?,?)",
                   [(1, "WhatsApp", "Gracias por tu compra de Playera local", "respondio"),
                    (3, "WhatsApp", "Hace tiempo no te vemos, tenemos novedades", "pendiente")])
    from .servicios import recalcular_cliente
    for (cid,) in db.execute("SELECT id_cliente FROM Cliente").fetchall():
        recalcular_cliente(db, cid)


@click.command("init-db")
@click.option("--vacia", is_flag=True, help="Crea las tablas sin datos de prueba")
def init_db_command(vacia):
    """Crea la base de datos del CRM."""
    init_db(con_datos=not vacia)
    click.echo("Base de datos lista.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
