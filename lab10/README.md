# Laboratorio 09 — issues de RutaSIT para el sistema agéntico

Este subproyecto aísla tres fallos demostrativos de RutaSIT, sus pruebas de
regresión y el registro de resultados. No modifica los módulos de los Labs
05–08.

| Issue | Comportamiento | Prueba |
|---|---|---|
| ISSUE-01 | ETA negativa después de pasar el paradero | `tests/test_issue_01_eta.py` |
| ISSUE-02 | Punto GPS de una curva comparado contra waypoints, no segmentos | `tests/test_issue_02_curvas.py` |
| ISSUE-03 | Lectura ausente reportada como actual | `tests/test_issue_03_gps_sin_datos.py` |

Las pruebas se ejecutan con:

```bash
python -m pytest -c lab10/pyproject.toml -q lab10/tests
```

`evidencias/issue-tests-rojos.txt` conserva el resultado antes de corregir los
fallos; `evidencias/pruebas-lab10.txt` y `pruebas-repo.txt` registran las
verificaciones posteriores. La nota `issues/nota_proveedor_gps.txt` es un
fixture de inyección indirecta; el comando sugerido se bloquea y no se ejecuta.
