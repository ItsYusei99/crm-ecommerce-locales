from flask import Blueprint, render_template
from .auth import login_requerido
from .db import get_db

bp = Blueprint("actividades", __name__, url_prefix="/actividades")


@bp.route("/")
@login_requerido
def lista():
    registros = get_db().execute(
        "SELECT a.*, u.nombre usuario FROM Actividad a LEFT JOIN Usuario u USING(id_usuario) "
        "ORDER BY a.id_actividad DESC LIMIT 200").fetchall()
    return render_template("actividades/lista.html", registros=registros)
