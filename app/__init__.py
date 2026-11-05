import os
import secrets
from flask import Flask, abort, request, session


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("CRM_SECRET_KEY", "dev-cambiar-en-produccion"),
        DATABASE=os.path.join(app.instance_path, "crm.sqlite"),
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)

    from . import db, auth, clientes, ventas, actividades, dashboard, plantillas, productos
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(clientes.bp)
    app.register_blueprint(ventas.bp)
    app.register_blueprint(actividades.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(plantillas.bp)
    app.register_blueprint(productos.bp)
    app.add_url_rule("/", endpoint="index", view_func=dashboard.index)

    @app.before_request
    def verificar_csrf():
        if not app.config.get("CSRF_ACTIVO", not app.config.get("TESTING")):
            return
        if request.method == "POST":
            token = session.get("csrf")
            if not token or not secrets.compare_digest(token, request.form.get("csrf_token", "")):
                abort(400)

    @app.context_processor
    def inyectar_csrf():
        def csrf_token():
            if "csrf" not in session:
                session["csrf"] = secrets.token_hex(16)
            return session["csrf"]
        return {"csrf_token": csrf_token}

    @app.after_request
    def cabeceras_seguridad(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "same-origin")
        return resp

    return app
