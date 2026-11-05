from datetime import date
from flask import Blueprint, current_app, render_template

bp = Blueprint("legal", __name__)
ACTUALIZADO = date(2026, 11, 4)


@bp.route("/privacidad")
def privacidad():
    return render_template("privacidad.html", actualizado=ACTUALIZADO,
                           contacto=current_app.config["PRIVACIDAD_CONTACTO"],
                           responsable=current_app.config["RESPONSABLE"])
