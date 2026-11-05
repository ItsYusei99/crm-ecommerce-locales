"""Genera un script SQL con los datos de SQLite listo para cargar en MySQL.

Uso: python scripts/migrar_a_mysql.py [ruta_sqlite] > datos_mysql.sql
Despues: mysql -u usuario -p < docs/mysql/schema_mysql.sql && mysql -u usuario -p crm_ecommerce < datos_mysql.sql
"""
import sqlite3
import sys

# Orden que respeta las llaves foraneas.
TABLAS = ["Usuario", "Cliente", "Producto", "Pedido", "DetallePedido", "Interaccion", "Actividad", "Plantilla"]


def literal(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return repr(v)
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def generar(ruta):
    con = sqlite3.connect(ruta)
    con.row_factory = sqlite3.Row
    salida = ["USE crm_ecommerce;", "SET FOREIGN_KEY_CHECKS=0;"]
    for t in TABLAS:
        filas = con.execute(f"SELECT * FROM {t}").fetchall()
        for f in filas:
            cols = ", ".join(f.keys())
            vals = ", ".join(literal(f[k]) for k in f.keys())
            salida.append(f"INSERT INTO {t} ({cols}) VALUES ({vals});")
    salida.append("SET FOREIGN_KEY_CHECKS=1;")
    return "\n".join(salida) + "\n"


if __name__ == "__main__":
    sys.stdout.write(generar(sys.argv[1] if len(sys.argv) > 1 else "instance/crm.sqlite"))
