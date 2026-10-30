from app.db import get_db


def test_dashboard(admin):
    html = admin.get("/").get_data(as_text=True)
    assert "Ventas por canal" in html and "Ana Lopez" in html


def test_alta_y_busqueda_cliente(admin):
    admin.post("/clientes/nuevo", data={"nombre": "Pedro Gil", "telefono_wa": "5215500000000"})
    html = admin.get("/clientes/?q=Pedro").get_data(as_text=True)
    assert "Pedro Gil" in html and "Ana Lopez" not in html


def test_telefono_duplicado(admin):
    r = admin.post("/clientes/nuevo", data={"nombre": "Otra", "telefono_wa": "5215512345678"})
    assert "Ya existe" in r.get_data(as_text=True)


def test_venta_actualiza_ltv_y_segmento(admin, app):
    admin.post("/ventas/nuevo", data={"id_cliente": 2, "id_producto": 2, "cantidad": 2, "canal": "IG"})
    with app.app_context():
        c = get_db().execute("SELECT ltv FROM Cliente WHERE id_cliente=2").fetchone()
        assert c["ltv"] == 998


def test_cancelar_venta_resta_ltv(admin, app):
    admin.post("/ventas/2/estado", data={"estado": "cancelado"})
    with app.app_context():
        assert get_db().execute("SELECT ltv FROM Cliente WHERE id_cliente=1").fetchone()["ltv"] == 598


def test_contacto_y_bitacora(admin):
    admin.post("/clientes/2/contacto", data={"tipo": "WhatsApp", "mensaje": "Seguimiento", "resultado": "respondio"})
    assert "Seguimiento" in admin.get("/clientes/2").get_data(as_text=True)
    assert "contacto" in admin.get("/actividades/").get_data(as_text=True)


def test_no_borra_cliente_con_pedidos(admin):
    r = admin.post("/clientes/1/eliminar", follow_redirects=True)
    assert "No se puede borrar" in r.get_data(as_text=True)


def test_link_whatsapp_en_ficha(admin):
    assert "https://wa.me/5215512345678" in admin.get("/clientes/1").get_data(as_text=True)
