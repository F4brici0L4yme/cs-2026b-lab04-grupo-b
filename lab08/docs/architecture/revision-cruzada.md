# E3 — Guion de revisión cruzada

Esta plantilla se completa **después de leer el repositorio asignado**. Los
hallazgos propios de RutaSIT no deben copiarse como si aplicaran al otro caso.

## Texto para el issue al otro grupo

**Título:** `E3 Lab08 — evaluación ATAM-lite del Grupo B`

- Grupo evaluado: pendiente.
- Commit revisado: pendiente.
- Árbol e iteración 1 revisados: enlaces pendientes.
- Evaluadores: nombres de integrantes que efectivamente revisaron.

| Tipo requerido | Hallazgo concreto | Escenario | Archivo/resultado que lo respalda | Pregunta / recomendación |
|---|---|---|---|---|
| Sensibilidad (≥1) | Completar | | | |
| Trade-off (≥1) | Completar | | | |
| Riesgo 1 (P/I 1–5) | Completar | | | |
| Riesgo 2 (P/I 1–5) | Completar | | | |
| No riesgo (≥1) | Completar | | | |

Antes de publicar: verificar que cada afirmación aparece en el modelo, código,
supuestos o resultados del grupo evaluado. Pedir evidencia faltante, sin asumir
que ausencia de una medida equivale a incumplimiento demostrado.

## Respuesta al issue recibido

Copiar cada hallazgo original a `atam-lite.md`. Para cada uno indicar:

1. Aceptado, parcialmente aceptado o refutado.
2. Evidencia concreta y enlace a commit/archivo/resultado.
3. Si es crítico: iteración que lo mitiga, prueba y riesgo residual.
4. Si se acepta sin mitigación: restricción y fecha/condición de revisión.

## Publicación (cuando exista el repositorio asignado)

```bash
gh issue create --repo ORGANIZACION/REPOSITORIO-ASIGNADO \
  --title 'E3 Lab08 — evaluación ATAM-lite del Grupo B' \
  --body-file evaluacion-verificada.md
```

`evaluacion-verificada.md` debe contener hallazgos reales, no esta plantilla.
