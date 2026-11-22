# ISSUE-02: una lectura sobre una curva se marca fuera de ruta

**Observado:** la verificación basada solo en puntos de control puede marcar
como desvío una ubicación GPS que está cerca del segmento curvo entre dos
puntos del trazado.

**Esperado:** comparar la ubicación con cada segmento del trazado y marcar
desvío solo cuando la distancia mínima excede la tolerancia.

**Pruebas de regresión:** `lab10/tests/test_issue_02_curvas.py`.

```bash
PYTHONPATH=lab10/caso_rutasit/src python -m pytest -q lab10/tests/test_issue_02_curvas.py
```
