import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("CRM_SECRET_KEY", "dev-cambiar-en-produccion"),
        DATABASE=os.path.join(app.instance_path, "crm.sqlite"),
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)

    from . import db, auth, clientes, ventas, actividades, dashboard
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(clientes.bp)
    app.register_blueprint(ventas.bp)
    app.register_blueprint(actividades.bp)
    app.register_blueprint(dashboard.bp)
    app.add_url_rule("/", endpoint="index", view_func=dashboard.index)
    return app
