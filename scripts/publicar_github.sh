#!/usr/bin/env bash
# Sube el repo a GitHub y crea labels, milestones (beta, rc) e issues con descripcion, analisis y solucion.
# Requiere GitHub CLI: brew install gh && gh auth login
set -euo pipefail
REPO="${1:-crm-ecommerce-locales}"
cd "$(dirname "$0")/.."

gh repo create "$REPO" --public --source . --remote origin --push
git push origin --all
git push origin --tags
OWNER_REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"

for l in "requisito:1c3454" "bug:c0392b" "backend:009688" "frontend:7b61ff" "ci:b26b00"; do
  gh label create "${l%%:*}" --color "${l##*:}" --force
done

gh api "repos/$OWNER_REPO/milestones" -f title=beta -f description="v0.7.0-beta: modulos principales y CI" -f due_on=2026-10-27T05:00:00Z -f state=closed >/dev/null
gh api "repos/$OWNER_REPO/milestones" -f title=rc -f description="v0.9.0-rc: plantillas, exportar, catalogo, MySQL" -f due_on=2026-11-17T05:00:00Z >/dev/null

issue() { # titulo milestone labels cerrar descripcion analisis solucion
  local url
  url=$(gh issue create --title "$1" --milestone "$2" --label "$3" \
    --body "$(printf '## Descripcion\n%s\n\n## Analisis\n%s\n\n## Solucion\n%s\n' "$5" "$6" "$7")")
  [ "$4" = "si" ] && gh issue close "$url" --comment "Implementado y probado (pytest en verde)."
  true
}

issue "RF-06 Registro y login de usuarios" beta "requisito,backend" si \
  "El emprendedor y su equipo necesitan entrar con su propia cuenta." \
  "Tabla Usuario ya existe en el modelo. Hay que guardar la contrasena con hash y manejar sesion." \
  "Blueprint auth: /auth/registro y /auth/login con werkzeug.security y sesion de Flask. El primer usuario es admin."
issue "RNF Seguridad basica: hash de contrasenas y roles" beta "requisito,backend" si \
  "Solo usuarios autenticados acceden y solo admin borra o cambia roles." \
  "Roles admin, editor y colaborador definidos en la Fase II." \
  "Decoradores login_requerido y rol_requerido; contrasena minima de 8 caracteres; SECRET_KEY por variable de entorno."
issue "RF-01 Gestion de clientes" beta "requisito,frontend" si \
  "Alta, edicion, busqueda y ficha del cliente con historial y LTV." \
  "WhatsApp es unico por cliente. No se debe borrar un cliente con pedidos." \
  "Blueprint clientes con CRUD, filtro por segmento y busqueda por nombre, WhatsApp o Instagram."
issue "RF-03 Gestion de contactos (interacciones)" beta "requisito,frontend" si \
  "Registrar cada contacto con el cliente (WhatsApp, IG, llamada) y su resultado." \
  "Tabla Interaccion de la Fase II. Hace falta un formulario en la ficha." \
  "Formulario en la ficha del cliente y botones wa.me con plantillas de gracias, reactivar y resena."
issue "RF-02 Seguimiento de ventas (pipeline)" beta "requisito,backend" si \
  "Ver los pedidos por estado y moverlos (nuevo, pagado, enviado, entregado, cancelado)." \
  "El LTV y el segmento del cliente cambian con cada venta o cancelacion." \
  "Blueprint ventas con tablero por estado; servicios.recalcular_cliente actualiza LTV y segmento."
issue "Registro de actividades (bitacora)" beta "requisito,backend" si \
  "Saber quien hizo que dentro del CRM." \
  "Nueva tabla Actividad (usuario, fecha, accion, detalle)." \
  "servicios.registrar_actividad en login, altas, ventas, contactos y cambios de rol; vista /actividades."
issue "RF-05 Dashboard con KPIs" beta "requisito,frontend" si \
  "Resumen del negocio al entrar." \
  "KPIs definidos en Fase II: ventas, ticket, recompra, inactivos, ventas por canal." \
  "Vista dashboard con tarjetas de KPI, barras por canal y top 5 clientes por LTV."
issue "Integracion continua con Travis CI y Drone" beta "ci" si \
  "Correr pruebas automaticas en cada push y PR." \
  "Pruebas con pytest y base temporal por prueba." \
  ".travis.yml (Python 3.11 y 3.12) y .drone.yml (imagen python:3.12-slim)."
issue "Plantillas de WhatsApp editables" rc "requisito,frontend" no \
  "El editor quiere cambiar los textos de postventa." "Hoy estan fijas en servicios.PLANTILLAS." "Tabla Plantilla y pantalla de edicion para rol editor."
issue "Exportar clientes a CSV/Excel" rc "requisito,frontend" no \
  "RNF de la Fase II: exportar datos." "Respetar filtros de la lista." "Ruta /clientes/exportar que devuelve CSV."
issue "Catalogo de productos (CRUD)" rc "requisito,backend" no \
  "Dar de alta productos sin tocar la BD." "Tabla Producto ya existe." "Blueprint productos con CRUD para admin y editor."
issue "Migrar de SQLite a MySQL" rc "backend" no \
  "Produccion usara MySQL como se decidio en la Fase II." "El esquema ya es equivalente a CRM_BD.sql." "Leer DATABASE_URL y usar PyMySQL; mantener SQLite para pruebas."

echo "Listo: https://github.com/$OWNER_REPO"
