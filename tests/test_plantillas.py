from app.db import get_db
from conftest import entrar


def test_editar_plantilla_cambia_el_link_de_la_ficha(admin):
    admin.post("/plantillas/", data={"clave": "gracias", "texto": "Mil gracias {nombre}!"})
    html = admin.get("/clientes/1").get_data(as_text=True)
    assert "Mil%20gracias%20Ana%21" in html


def test_crear_y_eliminar_plantilla(admin, app):
    admin.post("/plantillas/", data={"clave": "Cumple años", "texto": "Feliz cumple {nombre}"})
    with app.app_context():
        assert get_db().execute("SELECT texto FROM Plantilla WHERE clave='cumple_años'").fetchone()
    admin.post("/plantillas/cumple_años/eliminar")
    with app.app_context():
        assert get_db().execute("SELECT 1 FROM Plantilla WHERE clave='cumple_años'").fetchone() is None


def test_plantilla_vacia_se_rechaza(admin):
    assert "obligatorios" in admin.post("/plantillas/", data={"clave": "x", "texto": " "},
                                         follow_redirects=True).get_data(as_text=True)


def test_colaborador_no_edita_plantillas(client):
    client.post("/auth/registro", data={"nombre": "Col", "correo": "col@crm.local", "password": "demo12345"})
    entrar(client, "col@crm.local", "demo12345")
    assert client.get("/plantillas/").status_code == 403
