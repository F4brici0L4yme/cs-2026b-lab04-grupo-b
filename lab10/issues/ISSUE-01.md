# ISSUE-01: el ETA se vuelve negativo después de pasar el paradero

**Observado:** si el bus ya pasó el paradero, la distancia dirigida puede ser
negativa y el reporte calcula un ETA negativo.

**Esperado:** un bus que ya pasó el paradero debe informar ETA `0`, no un tiempo
de llegada negativo.

**Prueba de regresión:** `lab10/tests/test_issue_01_eta.py`.

```bash
PYTHONPATH=lab10/caso_rutasit/src python -m pytest -q lab10/tests/test_issue_01_eta.py
```
