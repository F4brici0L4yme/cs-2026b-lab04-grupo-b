# E1 — Catálogo MCP de RutaSIT Arequipa

| Capacidad | Primitiva | ¿Escribe? | Contrato y justificación |
|---|---|---:|---|
| Unidades activas de una ruta | `buses_en_ruta` | No | Recibe `R-01` o `R-02`; devuelve bus, estado y siguiente paradero. El modelo elige el filtro. |
| ETA publicado | `tiempo_llegada` | No | Recibe `bus_id` y `paradero_id` `P-NN`; devuelve salida estructurada con ETA y estado. |
| Reporte operativo de un desvío | `reportar_desvio` | Sí | Recibe bus, ruta y evidencia de 20–500 caracteres. Solo crea `reportes/DESVIO-NN.md`; no edita ni borra. |
| Mapa y reglas estables | Recursos | No | El host decide cuándo incorporar `rutasit://mapa/rutas` y `rutasit://reglas/operacion`. |
| Decisión arquitectónica | Recurso plantilla | No | `rutasit://adr/{numero}` exige tres dígitos y bloquea traversal de rutas. |
| Comunicar incidencia | Prompt `aviso_usuarios` | No | Plantilla que el usuario invoca con ruta y estado confirmado. |

La escritura está limitada a crear un artefacto nuevo con numeración correlativa.
No altera telemetría, rutas, código ni reportes existentes, por lo que puede
revisarse y revertirse eliminando solamente el reporte creado.
