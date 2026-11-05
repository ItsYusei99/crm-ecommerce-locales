# Pruebas funcionales y corrección de errores (Actividad 13)

## Estrategia

- **Pruebas automatizadas con pytest** sobre el cliente de pruebas de Flask y una base SQLite temporal con los datos de prueba. Se ejecutan en cada push con Travis CI y Drone.
- **Casos por módulo:** flujo normal, entradas inválidas, permisos por rol y seguridad.
- **Método:** primero se escribieron las pruebas de robustez (`tests/test_robustez.py`), se corrieron contra el código de la Fase III para detectar fallas reales y después se corrigió cada una hasta ponerlas en verde.

## Resultado global

| Momento | Pruebas | Pasan | Fallan |
|---|---|---|---|
| Fase III (beta) | 13 | 13 | 0 |
| Pruebas de robustez contra el código de la Fase III | 28 | 15 | **13** |
| Después de las correcciones | 28 | 28 | 0 |
| Fase IV final (con módulos nuevos) | 49 | 49 | 0 |

## Matriz de casos

| ID | Módulo | Caso | Resultado esperado | Estado |
|---|---|---|---|---|
| CP-01 | Acceso | Registro con contraseña de menos de 8 caracteres | Se rechaza con mensaje | Pasa |
| CP-02 | Acceso | Login con credenciales incorrectas | No inicia sesión | Pasa |
| CP-03 | Acceso | Primer usuario registrado | Queda como admin | Pasa |
| CP-04 | Acceso | Rutas protegidas sin sesión | Redirige al login | Pasa |
| CP-05 | Roles | Colaborador intenta eliminar cliente, exportar, editar plantillas o crear productos | 403 | Pasa |
| CP-06 | Roles | Usuario no admin abre `/auth/usuarios` | 403 | Pasa |
| CP-07 | Roles | Cambiar rol a un valor inexistente | Mensaje de error, sin cambios | Pasa |
| CP-08 | Roles | Degradar al último admin | Se bloquea | Pasa |
| CP-09 | Clientes | Alta y búsqueda por nombre | Aparece solo el cliente buscado | Pasa |
| CP-10 | Clientes | WhatsApp duplicado al crear o al editar | Mensaje "Ya existe…" | Pasa |
| CP-11 | Clientes | Teléfono con letras al crear o editar | Mensaje de validación | Pasa |
| CP-12 | Clientes | Búsqueda con `%` | Se trata como texto, no como comodín | Pasa |
| CP-13 | Clientes | 60 clientes nuevos | Listas de 25 por página | Pasa |
| CP-14 | Clientes | Eliminar cliente con pedidos | Se impide | Pasa |
| CP-15 | Contactos | Registrar contacto válido | Aparece en la ficha y en la bitácora | Pasa |
| CP-16 | Contactos | Tipo de contacto inventado | No se guarda | Pasa |
| CP-17 | Ventas | Pedido nuevo | Actualiza LTV y segmento | Pasa |
| CP-18 | Ventas | Cancelar pedido | Resta del LTV | Pasa |
| CP-19 | Ventas | Cantidad no numérica, cliente inexistente o canal inválido | Mensaje de error, sin error 500 | Pasa |
| CP-20 | Ventas | Cambiar estado de un pedido que no existe | 404 | Pasa |
| CP-21 | Plantillas | Editar el texto de una plantilla | El enlace de WhatsApp usa el texto nuevo | Pasa |
| CP-22 | Plantillas | Crear, eliminar y guardar vacía | Funciona; la vacía se rechaza | Pasa |
| CP-23 | Exportar | CSV completo y con filtro | Solo las filas filtradas | Pasa |
| CP-24 | Exportar | Cliente con nombre `=HYPERLINK(...)` | Se neutraliza con `'` | Pasa |
| CP-25 | Catálogo | Alta, edición, precio negativo, tipo inválido | Valida y guarda | Pasa |
| CP-26 | Catálogo | Producto desactivado | No se puede vender y conserva su historial | Pasa |
| CP-27 | Migración | Script a MySQL | Genera `INSERT` de todas las tablas | Pasa |
| CP-28 | Seguridad | POST sin token CSRF | 400 | Pasa |
| CP-29 | Seguridad | Cabeceras `X-Content-Type-Options` y `X-Frame-Options` | Presentes | Pasa |
| CP-30 | Legal | Aviso de privacidad sin iniciar sesión | Público y enlazado en el pie | Pasa |

## Bitácora de errores encontrados y corregidos

| ID | Error | Gravedad | Causa | Corrección |
|---|---|---|---|---|
| E-01 | Pedido con datos no numéricos devolvía error 500 | Alta | `int()` sin manejar la excepción | Validación con mensaje al usuario |
| E-02 | Pedido con cliente inexistente devolvía error 500 | Alta | Violación de llave foránea sin validar | Se comprueba que el cliente exista |
| E-03 | Pedido con canal inválido devolvía error 500 | Media | Restricción `CHECK` de la BD sin validar antes | Lista de canales permitidos |
| E-04 | Cambiar estado de un pedido inexistente devolvía error 500 | Media | Resultado `None` sin revisar | `abort(404)` |
| E-05 | Editar cliente con un WhatsApp repetido devolvía error 500 | Alta | `IntegrityError` sin capturar | Se captura y se muestra mensaje |
| E-06 | Al editar, se aceptaban teléfonos con letras | Media | La edición no validaba, solo el alta | Misma validación en alta y edición |
| E-07 | Rol inválido en usuarios devolvía error 500 | Media | `CHECK` de la BD sin validar antes | Lista de roles permitidos |
| E-08 | Se podía dejar el sistema sin administradores | Alta | Sin regla de último admin | Se bloquea la degradación del último admin |
| E-09 | Contactos con tipo o resultado inventado | Baja | Valores del formulario sin validar | Listas de valores permitidos |
| E-10 | Buscar `%` devolvía todos los clientes | Baja | Comodines de `LIKE` sin escapar | `ESCAPE` y función `patron_like` |
| E-11 | Formularios sin protección CSRF | Alta | Faltaba token por sesión | Token en cada formulario y verificación en `POST` |
| E-12 | La lista de clientes cargaba todos los registros | Media | Sin paginación | 25 por página con `LIMIT/OFFSET` |
| E-13 | Respuestas sin cabeceras de seguridad | Baja | Configuración por defecto | `nosniff`, `DENY` y `Referrer-Policy` |

## Cómo reproducir

```bash
python -m pytest -v
```
