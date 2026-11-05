# Evaluación y retroalimentación (Actividad 16)

## 1. Análisis de productividad

Datos tomados del repositorio, de los issues y de las mediciones del proyecto.

| Indicador | Fase III (beta) | Fase IV (final) |
|---|---|---|
| Módulos funcionales | 6 de 8 (70 %) | 7 de 8; el 8.º (MySQL y despliegue) quedó con esquema y script de migración, falta el servidor |
| Issues cerrados | 8 de 12 | 12 de 12 más 6 de la Fase IV |
| Pruebas automáticas | 13 | 49 |
| Líneas de código de la app | ~430 | ~680 |
| Líneas de pruebas | ~100 | ~330 |
| Errores encontrados y corregidos | — | 13 |
| Tiempo de la lista de clientes (5,000 registros) | 56 ms, 827 KB | 2 ms, 5.5 KB |
| Tiempo del tablero de ventas (20,000 pedidos) | 225 ms, 7.3 MB | 5 ms, 134 KB |
| Builds de CI | 1 en verde | pruebas en verde en cada push |

**Lectura de los datos**

- **Se cumplió antes de lo planeado:** el milestone *rc* tenía fecha del 16 de noviembre y sus 4 issues quedaron resueltos el 4 de noviembre.
- **Las pruebas crecieron más rápido que el código:** 3.8× más pruebas contra 1.6× más código. Escribirlas antes de corregir permitió ver que 13 de 28 casos fallaban en la versión anterior.
- **El mayor ahorro vino de medir:** dos cambios simples (índices y paginación) redujeron entre 4× y 47× el tiempo de las páginas pesadas.
- **Herramientas que ayudaron:** el tablero (Zube) para saber qué seguía, la integración continua para no romper lo ya hecho y los scripts (`publicar_github.sh`, `build_pages.py`) para no repetir tareas manuales.
- **Limitación:** los 19 commits del repositorio están registrados con un solo autor, por lo que el repositorio no refleja el trabajo de Emmanuel en la interfaz. Hay que acordar que cada integrante haga sus propios commits o pull requests.

## 2. Autoevaluación (Youssef)

Escala de 1 a 5. La evidencia sale del repositorio; ajusta la calificación si no coincide con tu percepción.

| Criterio | Evidencia | Calificación |
|---|---|---|
| Cumplimiento de entregables | Las 4 actividades de la Fase IV con su documento: pruebas, rendimiento, manual, aviso de privacidad, evaluación | 5 |
| Calidad técnica | 49 pruebas en verde, 13 errores corregidos, índices y paginación medidos | 5 |
| Uso de herramientas colaborativas | Issues, milestones, ramas por módulo, Zube y CI | 4 |
| Comunicación y trabajo en equipo | Reparto de responsabilidades documentado; faltó revisión cruzada con pull requests | 3 |
| Gestión del tiempo | Milestone rc terminado 12 días antes de su fecha | 4 |

**Qué hice bien:** automaticé lo repetitivo, medí antes de optimizar y dejé todo documentado para que otra persona pueda continuar.

**Qué debo mejorar:** pedir revisión del código antes de integrarlo y registrar mejor el trabajo de cada integrante.

## 3. Coevaluación

Cada integrante califica al otro de 1 a 5 y anota un comentario concreto. Se completa en equipo, no la rellena una sola persona.

| Criterio | Youssef evalúa a Emmanuel | Emmanuel evalúa a Youssef |
|---|---|---|
| Cumplió sus tareas en tiempo | ___ / 5 | ___ / 5 |
| Calidad de lo que entregó | ___ / 5 | ___ / 5 |
| Comunicación y disposición para ayudar | ___ / 5 | ___ / 5 |
| Uso de las herramientas del equipo | ___ / 5 | ___ / 5 |
| Comentario | | |

## 4. Propuestas de mejora

| Prioridad | Mejora | Beneficio |
|---|---|---|
| Alta | Despliegue en un servidor real con HTTPS (por ejemplo Render o Railway) | El CRM se usa desde cualquier dispositivo; hoy Pages solo muestra una demo |
| Alta | Usar MySQL en producción con el esquema y el script ya incluidos | Varios usuarios escribiendo a la vez y respaldos más robustos |
| Alta | Recuperación de contraseña y límite de intentos de inicio de sesión | Seguridad y menos soporte |
| Media | Pull requests con revisión cruzada y rama `main` protegida | Calidad y trazabilidad del trabajo de cada integrante |
| Media | Pedidos con varios productos | Refleja mejor las ventas reales |
| Media | Recordatorios automáticos para clientes inactivos | Más recompra sin trabajo manual |
| Baja | Integración con la API de WhatsApp Business | Enviar mensajes desde el CRM |
| Baja | Reportes por periodo y pruebas de interfaz en el CI | Mejores decisiones y menos regresiones |
