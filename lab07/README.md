# Laboratorio 07: patrones de diseño en RutaSIT Arequipa

Refactor del flujo `consultar_seguimiento` (Lab 05) hacia patrones GoF, con IA aislada.

## Patrones de diseño (Lab 07)

| Olor | Patrón | Prueba |
|---|---|---|
| `if/elif` ETA | Strategy + Factory | `test_open_closed_nuevo_algoritmo_sin_modificar_servicio` |
| SDK GPS distintos | Adapter | `test_adapter_unifica_gps` |
| Reintentos duplicados | Decorator | `test_decorator_reintentos_solo_timeout` |
| Condicionales estado | State | `test_state_impide_transiciones_invalidas` |
| Avisos a mano | Observer | `test_observer_nuevo_suscriptor_sin_tocar_servicio` |
| LLM no confiable | Strategy + Decorator (caché) + Chain | `test_chain_bloquea_salida_invalida`, `test_decorator_cache_evita_llamadas_repetidas` |

Métricas: consultar C(18)→A(5), promedio B(7.0)→A(1.69), SLOC 89→239. Pruebas: `30 passed, 1 xfailed`.

```bash
cd lab07
uv venv .venv && uv pip install --python .venv/bin/python pytest radon
PYTHONPATH=src .venv/bin/python -m pytest -v
PYTHONPATH=src .venv/bin/python -m radon cc -s -a src/
```
