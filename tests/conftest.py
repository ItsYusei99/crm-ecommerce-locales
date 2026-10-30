import os
import tempfile
import pytest
from app import create_app
from app.db import init_db


@pytest.fixture
def app():
    fd, ruta = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": ruta, "SECRET_KEY": "test"})
    with app.app_context():
        init_db()
    yield app
    os.close(fd)
    os.unlink(ruta)


@pytest.fixture
def client(app):
    return app.test_client()


def entrar(client, correo="youssef@crm.local", password="demo1234"):
    return client.post("/auth/login", data={"correo": correo, "password": password})


@pytest.fixture
def admin(client):
    entrar(client)
    return client
