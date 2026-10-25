# Bitácora IA (E7) — 5 interacciones, la IA propone, el equipo decide

| # | Prompt (resumen) | Propuesta IA | Verificación | Decisión |
|---|---|---|---|---|
| 1 | Detector de olores (antes + radon) | 8 olores y patrones, incluye Singleton | Revisión con radon y código | 6 aceptados, 2 rechazados |
| 2 | Refactor solo ETA+GPS | `ConReintentos` que reintenta todo | Prueba `test_sin_senal` en rojo (reintentaba rechazos) | Corregida: solo `TimeoutError` |
| 3 | Refactor estados | Tabla dict de transiciones | Válida, pero estados tendrán comportamiento propio | Rechazada a favor de State |
| 4 | Guardrails IA | Usar otro LLM como juez | Costo y latencia extra para MVP 1 mes | Rechazada; reglas deterministas |
| 5 | Diagramas PlantUML desde código | Clases y roles | Comparación con `pyreverse` y código real | Aceptada con correcciones de nombres |
| 6 | Revisión proveedor inválido | Validar después del cambio de estado | Prueba xfail en antes (`EN_RUTA` residual) | Aceptada: Factory valida antes en después |
