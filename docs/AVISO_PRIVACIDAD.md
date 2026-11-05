# Aviso de privacidad (Actividad 14)

La versión que usa el sistema está en `app/templates/privacidad.html` y se publica en la ruta pública `/privacidad`, con enlace en el pie de cada página. Esta es la misma información, resumida para la entrega.

## Responsable

El negocio que instale el CRM. Los datos de contacto se configuran con las variables de entorno `CRM_RESPONSABLE` y `CRM_PRIVACIDAD_CONTACTO`; hasta que se definan, la página lo indica con un texto de aviso.

## Datos que se recaban

| Titular | Datos |
|---|---|
| Clientes del negocio | Nombre, WhatsApp, Instagram, correo, pedidos, importes (LTV) y notas de contacto |
| Equipo que usa el CRM | Nombre, correo, rol y contraseña cifrada |
| Todos | Bitácora de acciones (quién, cuándo, qué) |

No se recaban datos sensibles ni financieros.

## Finalidades

- **Primarias:** pedidos, atención y postventa, cálculo del valor del cliente, control de acceso.
- **Secundarias:** promociones y recordatorios por WhatsApp o Instagram. El titular puede negarse sin afectar su atención.

## Derechos

Acceso, Rectificación, Cancelación y Oposición (ARCO) y revocación del consentimiento, mediante solicitud al contacto del responsable. Plazo de respuesta: 20 días hábiles. La cancelación no procede para datos que deban conservarse por obligaciones legales o fiscales.

## Medidas de seguridad

Contraseñas cifradas, acceso por roles, protección CSRF, cabeceras de seguridad, bitácora y una sola cookie de sesión.

## Marco legal

Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP). Este documento es una base para el proyecto escolar: antes de usar el CRM con clientes reales, el negocio debe completar sus datos de contacto y revisar el texto con un asesor legal.
