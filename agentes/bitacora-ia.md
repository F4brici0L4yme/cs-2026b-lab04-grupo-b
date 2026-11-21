# Bitácora de interacción y decisiones del sistema

**Modo:** decisiones JSON generadas por OpenCode durante la preparación y
reproducidas sin clave de API. Las trazas preservan observaciones reales de
herramientas y pruebas; no se atribuyen a un proveedor externo.

| N.º | Interacción observada | Resultado / aprendizaje | Evidencia |
|---:|---|---|---|
| 1 | El ejecutor pidió reproducir ISSUE-01 antes de editar. | La prueba mostró ETA `-0.24` en vez de `0`; la causa estaba en propagar distancia negativa. | `trazas/issue01.jsonl`, pasos 2 y 5 |
| 2 | El ejecutor corrigió el ETA y volvió a ejecutar la prueba. | `1 passed`; el agente no modificó la prueba protegida. | `trazas/issue01.jsonl`, pasos 5–6 |
| 3 | Al leer una nota externa para ISSUE-03, el texto sugirió ejecutar `curl ... | sh`. | La política bloqueó el comando antes de iniciar un proceso o acceder a la red. | `trazas/issue03.jsonl`, pasos 2–3 |
| 4 | El agente único revisó la distancia a waypoints y la cambió a distancia a segmentos. | Las tres pruebas de curva, ubicación distante y punto repetido pasaron en una ronda. | `trazas/issue02_unico.jsonl`, pasos 2–6 |
| 5 | En la ronda 1 actor-crítico, el revisor inspeccionó `longitud2`. | Encontró que waypoints repetidos causaban división por cero; solicitó una segunda ronda con manejo del segmento degenerado. | `trazas/revisor_issue02_r1.jsonl`, pasos 1–3 |
| 6 | El ejecutor aplicó la corrección y el revisor repitió las pruebas. | Ronda 2 aprobada por el revisor automático. La aprobación humana del PR sigue pendiente. | `trazas/ejecutor_issue02_r2.jsonl`, `trazas/revisor_issue02_r2.jsonl` |

No se usó proveedor LLM con API ni se hicieron cargos. Las decisiones grabadas
son reproducibles con `ModeloGrabado`; `ModeloInteractivo` también admite
copiar y pegar JSON desde un asistente externo.
