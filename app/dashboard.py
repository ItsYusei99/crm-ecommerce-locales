from flask import Blueprint, render_template
from .auth import login_requerido
from .db import get_db

bp = Blueprint("dashboard", __name__)


@login_requerido
def index():
    db = get_db()
    kpi = db.execute(
        "SELECT COALESCE(SUM(total),0) ventas, COUNT(*) pedidos, COALESCE(AVG(total),0) ticket "
        "FROM Pedido WHERE estado != 'cancelado'").fetchone()
    total_clientes = db.execute("SELECT COUNT(*) FROM Cliente").fetchone()[0]
    recompra = db.execute("SELECT COUNT(*) FROM Cliente WHERE segmento='frecuente'").fetchone()[0]
    inactivos = db.execute("SELECT COUNT(*) FROM Cliente WHERE segmento='inactivo'").fetchone()[0]
    por_canal = db.execute(
        "SELECT canal, COALESCE(SUM(total),0) monto FROM Pedido WHERE estado != 'cancelado' GROUP BY canal").fetchall()
    top = db.execute("SELECT id_cliente, nombre, ltv FROM Cliente ORDER BY ltv DESC LIMIT 5").fetchall()
    maximo = max([r["monto"] for r in por_canal] or [1])
    return render_template("dashboard.html", kpi=kpi, total_clientes=total_clientes,
                           recompra_pct=round(100 * recompra / total_clientes) if total_clientes else 0,
                           inactivos=inactivos, por_canal=por_canal, maximo=maximo, top=top)
