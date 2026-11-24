# Bitácora IA

| Interacción | Resultado y verificación |
|---|---|
| Diseñar catálogo MCP | Se eligieron las tres capacidades del caso 6 de la guía. |
| Reutilizar dominio | El servidor llama a `dominio.py`; no contiene consultas mezcladas con protocolo. |
| Validar salida estructurada | `tiempo_llegada` publica schema de `TypedDict`. |
| Revisar escritura | Se corrigió la sugerencia inicial de editar issues: el reporte crea `reportes/DESVIO-NN.md`. |
| Probar SDK MCP 2 | Se ajustó el cliente a modo `2026-07-28` y timeout explícito. |
| Completar E4/E6 | Se creó el adaptador que descubre el catálogo y una ejecución con traza JSONL y aprobación explícita de escritura. |
| Corregir contrato de escritura | Se detectó que el límite 20–500 solo estaba en el cuerpo de la función; se publicó con `Field` y se añadió su prueba. |
