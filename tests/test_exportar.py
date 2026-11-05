import csv
import io
from app.db import get_db
from conftest import entrar


def _filas(resp):
    return list(csv.reader(io.StringIO(resp.get_data(as_text=True).lstrip("\ufeff"))))


def test_exporta_todos_los_clientes(admin):
    r = admin.get("/clientes/exportar.csv")
    assert r.mimetype == "text/csv" and "attachment" in r.headers["Content-Disposition"]
    filas = _filas(r)
    assert filas[0][0] == "nombre" and len(filas) == 4


def test_exporta_respeta_el_filtro(admin):
    filas = _filas(admin.get("/clientes/exportar.csv?q=Ana"))
    assert [f[0] for f in filas[1:]] == ["Ana Lopez"]


def test_exportar_neutraliza_formulas(admin, app):
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO Cliente (nombre, telefono_wa) VALUES ('=HYPERLINK(\"x\")', '5211')")
        db.commit()
    assert any(f[0].startswith("'=") for f in _filas(admin.get("/clientes/exportar.csv")))


def test_colaborador_no_exporta(client):
    client.post("/auth/registro", data={"nombre": "Col", "correo": "col@crm.local", "password": "demo12345"})
    entrar(client, "col@crm.local", "demo12345")
    assert client.get("/clientes/exportar.csv").status_code == 403


def test_exportar_sin_sesion_redirige(client):
    assert client.get("/clientes/exportar.csv").status_code == 302
