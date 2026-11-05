import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from migrar_a_mysql import generar, literal, TABLAS


def test_literal_escapa_comillas_y_nulos():
    assert literal("O'Brien") == "'O''Brien'" and literal(None) == "NULL" and literal(5) == "5"


def test_migracion_genera_inserts_de_todas_las_tablas(app):
    sql = generar(app.config["DATABASE"])
    for t in ("Usuario", "Cliente", "Producto", "Pedido", "DetallePedido", "Interaccion", "Plantilla"):
        assert f"INSERT INTO {t} " in sql
    assert sql.count("INSERT INTO Cliente ") == 3 and "FOREIGN_KEY_CHECKS=0" in sql


def test_esquema_mysql_cubre_las_tablas_de_sqlite():
    ruta = os.path.join(os.path.dirname(__file__), "..", "docs", "mysql", "schema_mysql.sql")
    ddl = open(ruta).read()
    for t in TABLAS:
        assert f"CREATE TABLE {t} " in ddl
