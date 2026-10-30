"""Genera el sitio estatico para GitHub Pages: landing (pages/) + demo de solo lectura de la app.

Uso: python scripts/build_pages.py [carpeta_salida]
La demo se obtiene renderizando las vistas reales con el cliente de pruebas de Flask y datos de prueba.
"""
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import create_app  # noqa: E402
from app.db import get_db, init_db  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SALIDA = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "_site"))
BASE = os.environ.get("PAGES_BASE", "/crm-ecommerce-locales") + "/demo"

AVISO = ('<div class="aviso">Demo de solo lectura en GitHub Pages con datos de prueba. '
         'Los formularios estan desactivados; para usar el CRM completo correlo en local (ver README).</div>')
BLOQUEO = ("<style>form button, form input, form select, form textarea{pointer-events:none;opacity:.55}</style>"
           "<script>document.addEventListener('submit',e=>e.preventDefault(),true)</script>")


def a_estatico(html):
    # /clientes/1 -> BASE/clientes/1/ ; /static/x -> BASE/static/x
    def cambiar(m):
        attr, ruta = m.group(1), m.group(2)
        if ruta.startswith("/static/"):
            return f'{attr}="{BASE}{ruta}"'
        ruta = ruta.split("?")[0].rstrip("/")
        return f'{attr}="{BASE}{ruta}/"'
    html = re.sub(r'(href|action)="(/[^"]*)"', cambiar, html)
    html = html.replace("<main>", "<main>" + AVISO, 1).replace("</head>", BLOQUEO + "</head>", 1)
    return html


def guardar(ruta, html):
    destino = os.path.join(SALIDA, "demo", ruta.strip("/"), "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf8") as f:
        f.write(html)


def main():
    shutil.rmtree(SALIDA, ignore_errors=True)
    shutil.copytree(os.path.join(RAIZ, "pages"), SALIDA)
    shutil.copytree(os.path.join(RAIZ, "app", "static"), os.path.join(SALIDA, "demo", "static"))
    fd, bd = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": bd, "SECRET_KEY": "pages"})
    with app.app_context():
        init_db()
        ids = [r[0] for r in get_db().execute("SELECT id_cliente FROM Cliente")]
    c = app.test_client()
    c.post("/auth/login", data={"correo": "youssef@crm.local", "password": "demo1234"})
    rutas = ["/", "/clientes/", "/ventas/", "/ventas/nuevo", "/clientes/nuevo", "/actividades/", "/auth/usuarios"]
    rutas += [f"/clientes/{i}" for i in ids] + [f"/clientes/{i}/editar" for i in ids]
    for r in rutas:
        resp = c.get(r)
        assert resp.status_code == 200, (r, resp.status_code)
        guardar(r, a_estatico(resp.get_data(as_text=True)))
    for r in ["/auth/login", "/auth/registro", "/auth/logout"]:  # en la demo ya hay sesion iniciada
        guardar(r, f'<meta http-equiv="refresh" content="0; url={BASE}/">')
    open(os.path.join(SALIDA, ".nojekyll"), "w").close()
    os.close(fd)
    os.unlink(bd)
    print("Sitio generado en", SALIDA)


if __name__ == "__main__":
    main()
