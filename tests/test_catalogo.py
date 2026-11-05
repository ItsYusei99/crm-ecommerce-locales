from app.db import get_db
from conftest import entrar


def test_alta_de_producto(admin):
    admin.post("/productos/nuevo", data={"nombre": "Taza", "tipo": "fisico", "precio": "150.50"})
    assert "Taza" in admin.get("/productos/").get_data(as_text=True)


def test_precio_negativo_se_rechaza(admin):
    r = admin.post("/productos/nuevo", data={"nombre": "Taza", "tipo": "fisico", "precio": "-5"})
    assert "obligatorios" in r.get_data(as_text=True)


def test_tipo_invalido_se_rechaza(admin):
    r = admin.post("/productos/nuevo", data={"nombre": "Taza", "tipo": "otro", "precio": "5"})
    assert "obligatorios" in r.get_data(as_text=True)


def test_editar_precio(admin, app):
    admin.post("/productos/1/editar", data={"nombre": "Playera local", "tipo": "fisico", "precio": "350"})
    with app.app_context():
        assert get_db().execute("SELECT precio FROM Producto WHERE id_producto=1").fetchone()["precio"] == 350


def test_producto_inactivo_no_se_vende_y_conserva_historial(admin, app):
    admin.post("/productos/1/activo")
    assert "Playera local" not in admin.get("/ventas/nuevo").get_data(as_text=True)
    r = admin.post("/ventas/nuevo", data={"id_cliente": 1, "id_producto": 1, "cantidad": 1, "canal": "WA"})
    assert "invalid" in r.get_data(as_text=True).lower()
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM DetallePedido WHERE id_producto=1").fetchone()[0] == 2


def test_producto_inexistente(admin):
    assert admin.get("/productos/999/editar").status_code == 404


def test_colaborador_no_crea_productos(client):
    client.post("/auth/registro", data={"nombre": "Col", "correo": "col@crm.local", "password": "demo12345"})
    entrar(client, "col@crm.local", "demo12345")
    assert client.get("/productos/").status_code == 200
    assert client.post("/productos/nuevo", data={"nombre": "X", "tipo": "fisico", "precio": "1"}).status_code == 403
