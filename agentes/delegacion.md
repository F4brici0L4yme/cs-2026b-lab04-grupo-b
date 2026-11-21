# Delegación progresiva y humano en el circuito

La delegación aumenta solo después de revisar pruebas, trazas y seguridad. El
agente nunca aprueba ni fusiona su propio cambio. La integración al repositorio
queda en manos de una persona del grupo.

| Rol | Permisos del agente | Evidencia para avanzar | Decisión humana |
|---|---|---|---|
| Ejecutor | Lee y busca en el repositorio; edita únicamente `lab09/caso_rutasit/src/`; corre pytest y radon permitidos; registra notas. | Prueba del issue en verde, diff legible, sin editar pruebas ni salir del sandbox. | Aprueba o rechaza cada edición con `s` o `n`. |
| Revisor | Solo lectura, búsqueda, estado/diff y pruebas. No tiene `editar_archivo` ni `anotar`. | Revisión de límites, caso borde reproducido, pruebas pertinentes y conclusión trazable. | Solicita cambios o recomienda aprobación. |
| Colaborador | Puede preparar nuevos issues, pruebas y propuestas en una rama de trabajo; no puede saltarse la política del ejecutor. | Dos issues revisados, pruebas rojas/ verdes repetibles, cero accesos fuera del sandbox. | Revisa el alcance y autoriza ampliar una herramienta o ruta. |
| Gobernador | No recibe permisos autónomos de edición, red, publicación ni merge. El sistema puede generar evidencia y una propuesta de PR. | Historial de trazas completo, análisis de seguridad, suite verde, revisión cruzada registrada. | Aprueba manualmente el PR, la integración y la etiqueta de versión. |

## Activación de aprobación en consola

```bash
python -m agentes.ejecutar \
  --raiz . \
  --objetivo "Resuelve ISSUE-01 sin modificar sus pruebas." \
  --traza agentes/trazas/issue01_humano.jsonl \
  --interactivo \
  --aprobar-ediciones
```

La función de aprobación repite la pregunta hasta recibir exactamente `s` o
`n`. En esta entrega no se registró una aprobación humana real; la aprobación
del crítico es automática y no sustituye esa intervención.
