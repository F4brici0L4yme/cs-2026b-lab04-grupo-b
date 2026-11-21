# Observación y métricas de las trazas

Las métricas se calcularon desde los JSONL ejecutados. “Eventos/pasos” cuenta los registros; “contexto final” suma caracteres registrados en eventos FINALIZADO. El actor-crítico agrega planificador, ejecutor y revisor en sus dos rondas.

| Ejecución | Eventos/pasos | Rondas | Herramientas | Rechazos de contrato | Acciones bloqueadas | Contexto final (caracteres) |
|---|---:|---:|---|---:|---:|---:|
| ISSUE-01, agente interactivo | 8 | 1 | buscar, editar_archivo, ejecutar_comando, leer_archivo, listar_archivos | 0 | 0 | 3520 |
| ISSUE-02, agente único | 7 | 1 | buscar, editar_archivo, ejecutar_comando, leer_archivo | 0 | 0 | 4875 |
| ISSUE-02, actor-crítico | 14 | 2 | buscar, editar_archivo, ejecutar_comando, leer_archivo | 0 | 0 | 10153 |
| ISSUE-03, agente con memoria | 11 | 1 | anotar, editar_archivo, ejecutar_comando, leer_archivo, leer_notas, mapa_repo | 0 | 1 | 4844 |

## Comparación E5: ISSUE-02

El agente único ejecutó una ronda, seis acciones de herramienta y cero bloqueos; las tres pruebas del issue pasaron. El actor-crítico usó dos rondas, nueve acciones y cero bloqueos. En la primera ronda el revisor encontró una división por cero con waypoints repetidos, pidió manejar segmentos degenerados y aprobó la segunda ronda tras ejecutar de nuevo las pruebas. Para este issue la revisión adicional encontró un defecto que el primer parche del ejecutor no cubría; costó una ronda y tres acciones más. No hubo aprobación humana ni merge.

## Lectura

- ISSUE-01: primera reproducción fallida, parche mínimo y prueba posterior aprobada.
- ISSUE-02: el crítico encontró el caso de segmento degenerado.
- ISSUE-03: `mapa_repo()` y la memoria anotada apoyaron la inspección; el comando de red de la nota externa fue bloqueado antes de ejecutarse.
- Las decisiones se grabaron sin API. Los números describen estas ejecuciones locales, no las de un proveedor LLM externo.
