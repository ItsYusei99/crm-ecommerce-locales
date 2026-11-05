"""Pruebas funcionales de Fase IV: entradas invalidas, permisos y seguridad.

Cada prueba corresponde a un caso de docs/PRUEBAS_FUNCIONALES.md.
"""
from app.db import get_db
from conftest import entrar


def test_venta_con_datos_no_numericos(admin):
    r = admin.post("/ventas/nuevo", data={"id_cliente": "x", "id_producto": "1", "cantidad": "abc", "canal": "WA"})
    assert r.status_code == 200 and "invalid" in r.get_data(as_text=True).lower()


def test_venta_cliente_inexistente(admin):
    r = admin.post("/ventas/nuevo", data={"id_cliente": 999, "id_producto": 1, "cantidad": 1, "canal": "WA"})
    assert r.status_code == 200 and "invalid" in r.get_data(as_text=True).lower()


def test_venta_canal_invalido(admin):
    r = admin.post("/ventas/nuevo", data={"id_cliente": 1, "id_producto": 1, "cantidad": 1, "canal": "FAX"})
    assert r.status_code == 200 and "invalid" in r.get_data(as_text=True).lower()


def test_estado_de_pedido_inexistente(admin):
    assert admin.post("/ventas/999/estado", data={"estado": "pagado"}).status_code == 404


def test_editar_cliente_con_telefono_duplicado(admin):
    r = admin.post("/clientes/1/editar", data={"nombre": "Ana", "telefono_wa": "5215587654321"})
    assert r.status_code == 200 and "Ya existe" in r.get_data(as_text=True)


def test_editar_cliente_telefono_invalido(admin):
    r = admin.post("/clientes/1/editar", data={"nombre": "Ana", "telefono_wa": "abc"})
    assert r.status_code == 200 and "solo con numeros" in r.get_data(as_text=True)


def test_rol_invalido(admin):
    assert admin.post("/auth/usuarios", data={"id_usuario": 2, "rol": "dios"}).status_code == 200


def test_ultimo_admin_no_se_degrada(admin, app):
    admin.post("/auth/usuarios", data={"id_usuario": 1, "rol": "colaborador"})
    with app.app_context():
        assert get_db().execute("SELECT rol FROM Usuario WHERE id_usuario=1").fetchone()["rol"] == "admin"


def test_tipo_de_contacto_invalido(admin):
    r = admin.post("/clientes/1/contacto", data={"tipo": "Paloma", "mensaje": "hola"})
    assert r.status_code == 200 or r.status_code == 302
    assert "Paloma" not in admin.get("/clientes/1").get_data(as_text=True)


def test_busqueda_trata_comodines_como_texto(admin):
    html = admin.get("/clientes/?q=%25").get_data(as_text=True)
    assert "Ana Lopez" not in html


def test_post_sin_token_csrf_se_rechaza(app):
    c = app.test_client()
    entrar(c)
    app.config["CSRF_ACTIVO"] = True
    assert c.post("/clientes/nuevo", data={"nombre": "X", "telefono_wa": "1"}).status_code == 400


def test_colaborador_no_elimina_cliente(client):
    client.post("/auth/registro", data={"nombre": "Col", "correo": "col@crm.local", "password": "demo12345"})
    entrar(client, "col@crm.local", "demo12345")
    assert client.post("/clientes/3/eliminar").status_code == 403


def test_usuarios_solo_admin(client):
    entrar(client, "emma@crm.local")
    assert client.get("/auth/usuarios").status_code == 403


def test_paginacion_de_clientes(admin, app):
    with app.app_context():
        db = get_db()
        db.executemany("INSERT INTO Cliente (nombre, telefono_wa) VALUES (?,?)",
                       [(f"Cliente {i}", str(5200000000 + i)) for i in range(60)])
        db.commit()
    p1 = admin.get("/clientes/").get_data(as_text=True)
    p2 = admin.get("/clientes/?pagina=2").get_data(as_text=True)
    assert p1.count("<tr><td><a") == 25 and p2.count("<tr><td><a") == 25


def test_cabeceras_de_seguridad(admin):
    r = admin.get("/")
    assert r.headers["X-Content-Type-Options"] == "nosniff" and r.headers["X-Frame-Options"] == "DENY"
