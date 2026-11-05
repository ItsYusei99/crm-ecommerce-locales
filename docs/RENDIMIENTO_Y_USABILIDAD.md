# Mejora de rendimiento y usabilidad (Actividad 13)

## Rendimiento

**Cómo se midió:** base de prueba con 5,000 clientes y 20,000 pedidos, usuario admin autenticado, promedio de 20 peticiones por página con el cliente de pruebas de Flask (sin red). Las mismas pruebas se corrieron contra el commit `acc4158` (Fase III) y contra la versión final. Son tiempos del servidor en una laptop, no de producción.

| Página | Antes | Después | Mejora |
|---|---|---|---|
| Dashboard | 18.0 ms | 7.2 ms | 2.5× |
| Clientes (lista completa) | 56.4 ms · 827 KB | 2.1 ms · 5.5 KB | 27× más rápida, 150× menos datos |
| Clientes filtrados por segmento | 13.5 ms · 278 KB | 1.2 ms · 5.6 KB | 11× |
| Clientes con búsqueda de texto | 10.3 ms · 185 KB | 2.6 ms · 5.6 KB | 4× |
| Ventas (pipeline) | 224.8 ms · 7.3 MB | 4.8 ms · 134 KB | 47× más rápida, 54× menos datos |

**Qué se cambió:**
1. **Índices:** `Cliente(segmento, ltv)`, `Pedido(estado)`, `Pedido(canal)`, `Interaccion(id_cliente, fecha)` y `DetallePedido(id_pedido)`.
2. **Paginación** de 25 clientes por página, con contador y enlaces anterior/siguiente.
3. **Límite de 300 pedidos recientes** en el tablero de ventas.
4. **SQLite en modo WAL** y espera de 10 s ante bloqueos, para que lecturas y escrituras no se bloqueen entre sí.
5. **Filtro reutilizado** entre la lista y la exportación, para que ambas usen la misma consulta.

## Usabilidad

| Mejora | Qué resuelve |
|---|---|
| Mensajes de error claros en lugar de pantallas de error | El usuario sabe qué corregir |
| Paginación y contador de resultados | Listas largas fáciles de recorrer |
| Búsqueda tolerante a símbolos | `%` y `_` se buscan como texto |
| Plantillas de WhatsApp editables | Cada negocio usa su propio tono |
| Exportar clientes a CSV (abre en Excel con acentos) | Reportes y campañas fuera del CRM |
| Catálogo con baja lógica | Un producto se retira sin perder el historial de ventas |
| Confirmación al eliminar | Evita borrados por accidente |
| Foco visible con teclado | Accesibilidad |
| Tablas con desplazamiento horizontal y ajustes para móvil | Uso desde el celular |
| Aviso de privacidad accesible desde el pie de cada página | Transparencia con los datos |
