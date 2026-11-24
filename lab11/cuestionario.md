# Cuestionario — Lab 11

1. MCP reduce N×M adaptadores entre agentes y fuentes a N+M: RutaSIT publica una vez sus consultas y cualquier host compatible las descubre.
2. El host integra el LLM y permisos; cada conexión host-servidor usa un cliente; el servidor publica capacidades. Un host con tres servidores tiene tres clientes.
3. La consulta de ETA es una herramienta porque el modelo selecciona parámetros y recibe un resultado dinámico. Un ADR es recurso estable que el host incorpora por URI.
4. La versión 2026-07-28 elimina `initialize` y sesiones; cada petición lleva contexto de protocolo, lo que simplifica despliegues remotos sin estado.
5. `isError: true` es resultado de una herramienta y permite que el agente corrija argumentos. Un error JSON-RPC rechaza la petición de protocolo.
6. Las anotaciones son declaraciones del servidor, no garantías. La política deriva las escrituras y exige aprobación humana para `reportar_desvio`.
7. El costo se mide desde `tools/list`; el catálogo se limitó a tres herramientas con descripciones cortas y parámetros cerrados.
8. El envenenamiento oculta instrucciones hostiles en descripciones. Se mitiga auditando el catálogo, fijando servidores aprobados/versionados y limitando permisos con aprobación de escritura.
