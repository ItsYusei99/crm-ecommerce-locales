from flask import Blueprint, flash, redirect, render_template, request, url_for
from .auth import login_requerido, rol_requerido
from .db import get_db
from .servicios import plantillas_de, registrar_actividad

bp = Blueprint("plantillas", __name__, url_prefix="/plantillas")


@bp.route("/", methods=("GET", "POST"))
@rol_requerido("admin", "editor")
def lista():
    db = get_db()
    if request.method == "POST":
        clave = request.form.get("clave", "").strip().lower().replace(" ", "_")
        texto = request.form.get("texto", "").strip()
        if not clave or not texto or len(texto) > 500:
            flash("Clave y texto son obligatorios (maximo 500 caracteres).")
        else:
            db.execute("INSERT INTO Plantilla (clave, texto) VALUES (?,?) "
                       "ON CONFLICT(clave) DO UPDATE SET texto=excluded.texto", (clave, texto))
            registrar_actividad(db, "plantilla", clave)
            db.commit()
            flash("Plantilla guardada.")
        return redirect(url_for("plantillas.lista"))
    return render_template("plantillas/lista.html", plantillas=plantillas_de(db))


@bp.route("/<clave>/eliminar", methods=("POST",))
@rol_requerido("admin", "editor")
def eliminar(clave):
    db = get_db()
    db.execute("DELETE FROM Plantilla WHERE clave=?", (clave,))
    registrar_actividad(db, "plantilla_baja", clave)
    db.commit()
    return redirect(url_for("plantillas.lista"))
