from conftest import entrar


def test_registro_y_login(client):
    r = client.post("/auth/registro", data={"nombre": "Caro", "correo": "caro@crm.local", "password": "segura123"})
    assert r.status_code == 302
    assert entrar(client, "caro@crm.local", "segura123").headers["Location"] == "/"


def test_contrasena_corta(client):
    r = client.post("/auth/registro", data={"nombre": "X", "correo": "x@crm.local", "password": "123"})
    assert "al menos 8" in r.get_data(as_text=True)


def test_login_incorrecto(client):
    assert "incorrectos" in entrar(client, password="mala").get_data(as_text=True)


def test_rutas_protegidas(client):
    for ruta in ["/", "/clientes/", "/ventas/", "/actividades/"]:
        assert client.get(ruta).status_code == 302


def test_colaborador_no_administra_usuarios(client):
    client.post("/auth/registro", data={"nombre": "Col", "correo": "col@crm.local", "password": "segura123"})
    entrar(client, "col@crm.local", "segura123")
    assert client.get("/auth/usuarios").status_code == 403
    assert client.post("/clientes/2/eliminar").status_code == 403
