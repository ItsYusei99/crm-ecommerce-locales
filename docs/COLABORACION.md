# Uso de herramientas colaborativas (Actividad 14)

## Herramientas

| Herramienta | Para qué la usamos | Evidencia |
|---|---|---|
| **GitHub** | Repositorio, ramas, issues, milestones y etiquetas | github.com/ItsYusei99/crm-ecommerce-locales |
| **Git (flujo con ramas)** | `main` estable, `develop` integración, `feature/*` por módulo | `docs/FLUJO_GIT.md` |
| **Zube** | Tablero kanban conectado a los issues y sprint de cada milestone | `assets/evidencia_zube.png` |
| **Travis CI y Drone** | Correr pytest en cada push | `.travis.yml`, `.drone.yml`, `assets/evidencia_travis.png` |
| **GitHub Pages** | Landing y demo de solo lectura del CRM | itsyusei99.github.io/crm-ecommerce-locales |
| **Plantillas de issues y de PR** | Reportar errores y proponer mejoras con el mismo formato | `.github/` |

## Cómo trabajamos

1. Cada tarea es un **issue** con milestone (beta, rc, v1.0) y etiquetas (`requisito`, `bug`, `backend`, `frontend`, `ci`, `documentation`).
2. Cada issue sale en una **rama `feature/…`** (o `fix/…`) desde `develop`.
3. Los commits son cortos, en español y con prefijo (`feat:`, `fix:`, `test:`, `docs:`, `ci:`) y cierran el issue con `closes #N`.
4. Se hace **merge a `develop`** cuando las pruebas pasan; de `develop` se libera a `main` con un **tag** (`v0.7.0-beta`, `v0.9.0-rc`, `v1.0.0`).
5. Travis y Drone corren las pruebas en cada push; un build en rojo no se libera.

## Reparto

| Integrante | Responsabilidad |
|---|---|
| Youssef | Datos y backend: base de datos, acceso, ventas, CI, pruebas |
| Emmanuel | Frontend y UI: clientes, dashboard, vistas y estilos |

## Lo que haríamos distinto

- Abrir **pull requests con revisión cruzada**: en esta fase los merges se hicieron directamente en `develop` y el repositorio no tiene PRs registrados.
- Proteger `main` para exigir el build en verde antes de liberar.
