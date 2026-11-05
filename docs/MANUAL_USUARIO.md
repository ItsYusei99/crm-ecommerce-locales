# Manual de usuario del CRM (Actividad 14)

CRM para emprendedores que venden por Instagram, WhatsApp y tienda en línea. Reúne clientes, pedidos y mensajes en un solo lugar para vender más y dar mejor postventa.

## 1. Entrar al sistema

1. Abre la dirección del CRM en tu navegador.
2. **Primera vez:** pulsa *Crear cuenta*, escribe nombre, correo y una contraseña de al menos 8 caracteres. La primera cuenta del sistema es administradora; las demás son *colaborador* hasta que un admin cambie su rol.
3. **Ya tienes cuenta:** escribe correo y contraseña en *Iniciar sesión*.
4. Para salir, usa *Salir* en la barra superior.

### Qué puede hacer cada rol

| Acción | Colaborador | Editor | Admin |
|---|---|---|---|
| Ver dashboard, clientes, ventas, catálogo y actividades | Sí | Sí | Sí |
| Crear y editar clientes, registrar contactos | Sí | Sí | Sí |
| Crear pedidos y moverlos de estado | Sí | Sí | Sí |
| Exportar clientes a CSV | No | Sí | Sí |
| Editar plantillas de WhatsApp | No | Sí | Sí |
| Crear, editar y desactivar productos | No | Sí | Sí |
| Eliminar clientes | No | No | Sí |
| Administrar usuarios y roles | No | No | Sí |

## 2. Dashboard

Es la pantalla de inicio. Muestra ventas totales, número de pedidos, ticket promedio, porcentaje de clientes que recompran, clientes inactivos, ventas por canal (Instagram, WhatsApp, web) y los 5 clientes con más valor (LTV). Los pedidos cancelados no cuentan.

## 3. Clientes

1. **Buscar:** escribe nombre, WhatsApp o Instagram y pulsa *Filtrar*. También puedes filtrar por segmento.
2. **Agregar:** pulsa *+ Nuevo*. El nombre y el WhatsApp son obligatorios; el WhatsApp va con lada y solo números (ejemplo: `5215512345678`). No se permiten dos clientes con el mismo WhatsApp.
3. **Ver la ficha:** pulsa el nombre del cliente. Ahí ves sus datos, su LTV, sus pedidos y su historial de contactos.
4. **Editar:** *Editar* en la ficha.
5. **Eliminar (solo admin):** *Eliminar* en la ficha. No se puede borrar un cliente que ya tiene pedidos.
6. **Exportar (editor y admin):** *Exportar CSV* descarga la lista con el filtro que tengas aplicado. Abre el archivo con Excel o Google Sheets.
7. La lista muestra 25 clientes por página; usa *Anterior* y *Siguiente*.

### Segmentos

| Segmento | Cuándo se asigna |
|---|---|
| Nuevo | Sin compras o con una sola compra reciente |
| Frecuente | Dos o más compras y la última hace menos de 30 días |
| Inactivo | Su última compra fue hace más de 30 días |

El sistema los calcula solo cada vez que cambia un pedido.

## 4. Contactos y mensajes por WhatsApp

- En la ficha, la sección *Mensajes rápidos WhatsApp* tiene un botón por cada plantilla. Al pulsarlo se abre WhatsApp con el mensaje ya escrito y el nombre del cliente; tú solo lo envías.
- Después de hablar con un cliente, usa *Registrar contacto*: elige el medio (WhatsApp, Instagram, llamada o correo), anota qué se habló y el resultado (pendiente, respondió, compró, sin respuesta).

## 5. Plantillas de WhatsApp (editor y admin)

1. Entra a *Plantillas*.
2. Cambia el texto y pulsa *Guardar*. Escribe `{nombre}` donde quieras que aparezca el primer nombre del cliente.
3. Para crear una nueva, usa *Nueva plantilla* con una clave corta (ejemplo: `cumpleanos`).

## 6. Ventas

1. **Nuevo pedido:** pulsa *+ Nuevo pedido*, elige cliente, producto, cantidad y canal. El total y el LTV del cliente se calculan solos.
2. **Seguimiento:** el tablero tiene una columna por estado: nuevo → pagado → enviado → entregado (y cancelado). Para mover un pedido, elige el estado en su tarjeta y pulsa *Mover*.
3. Si cancelas un pedido, su importe deja de contar en el LTV del cliente.

## 7. Catálogo

Lista todos los productos con su tipo (físico o digital), precio y estado. Editores y admins pueden agregar, cambiar el precio o **desactivar** un producto: deja de ofrecerse en nuevos pedidos pero conserva su historial.

## 8. Actividades

Bitácora de lo que hace el equipo: quién, cuándo y qué (inicios de sesión, altas, ventas, contactos, cambios de rol). Se muestran las últimas 200.

## 9. Usuarios (solo admin)

Lista a todo el equipo y permite cambiar el rol de cada persona. Siempre debe quedar al menos un admin.

## 10. Problemas frecuentes

| Qué ves | Qué hacer |
|---|---|
| "Correo o contraseña incorrectos" | Revisa mayúsculas y que el correo esté bien escrito. Todavía no hay recuperación automática de contraseña; si la olvidaste, avisa al administrador. |
| "Ya existe un cliente con ese WhatsApp" | Busca al cliente; probablemente ya está registrado. |
| "Nombre obligatorio y teléfono solo con números" | Quita espacios, guiones y el signo `+` del teléfono. |
| "No se puede borrar un cliente con pedidos" | Es para conservar el historial de ventas. El cliente se mantiene y el sistema lo marca como inactivo si deja de comprar. |
| Error 403 | Tu rol no tiene permiso para esa acción; pide ayuda a un admin. |
| El botón de WhatsApp no abre la conversación | Verifica que el número tenga lada del país (52 para México). |

## 11. Instalación (para quien administra el sistema)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app init-db          # crea la base con datos de ejemplo (usa --vacia para empezar sin datos)
CRM_SECRET_KEY="una-clave-larga-y-secreta" flask --app app run
```

Define también `CRM_RESPONSABLE` y `CRM_PRIVACIDAD_CONTACTO` para el aviso de privacidad. Cambia las contraseñas de las cuentas de ejemplo antes de usar datos reales.
