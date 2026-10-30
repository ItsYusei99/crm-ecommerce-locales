# Flujo de trabajo con Git

## Ramas
- `main`: version estable, solo recibe merges desde `develop` o `release/*`.
- `develop`: integracion de los modulos.
- `feature/<modulo>`: una rama por modulo o issue (`feature/auth`, `feature/clientes`, ...).
- `release/<version>`: estabilizacion antes de un tag.

## Reglas
1. Cada cambio sale de un issue. El nombre de la rama lleva el modulo.
2. Commits cortos en espanol con prefijo: `feat:`, `fix:`, `test:`, `docs:`, `ci:`.
3. Pull request hacia `develop`, con `Cierra #N` y pruebas en verde en Travis/Drone.
4. El otro integrante revisa el PR antes del merge.

## Milestones
| Milestone | Version | Contenido | Fecha |
|---|---|---|---|
| beta | v0.7.0-beta | auth, clientes, contactos, ventas, actividades, dashboard, CI | 26 oct 2026 |
| rc | v0.9.0-rc | plantillas WhatsApp editables, exportar CSV, catalogo, MySQL | 16 nov 2026 |

## Reparto
| Integrante | Ramas |
|---|---|
| Youssef | feature/auth, feature/ventas, feature/actividades, feature/ci |
| Emmanuel | feature/clientes, feature/dashboard, vistas y CSS |
