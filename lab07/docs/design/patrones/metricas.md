# Métricas y trade-off (E6) — radon 6.0.1

## Complejidad ciclomática

| Método | Antes | Después |
|---|---|---|
| `consultar_seguimiento` | C (18) | A (5) |
| `explicar_retraso` | B (7) | A (2) |
| Promedio módulo | B (7.0) | A (1.69) |

## Líneas (SLOC, `radon raw -s`)

| Versión | SLOC |
|---|---|
| `antes/servicio.py` | 89 |
| `servicio.py + eta.py + estados.py + eventos.py + ia.py` | 239 |

Pruebas: `30 passed, 1 xfailed` (el xfail documenta bug corregido: antes dejaba `EN_RUTA` con proveedor inválido).

## Trade-off

Ganamos complejidad 18→5 y promedio 7.0→1.69; agregar un GPS o algoritmo ya no toca el servicio. Costó pasar de 89 a 239 SLOC y de 1 a 5 archivos, con más indirección. Si RutaSIT solo tuviera un GPS y un algoritmo sin IA, la versión antes bastaba. Los patrones se justifican por los cambios previstos (2 operadores, 2 ETAs, IA con guardrails), no por sí mismos.

## Patrón rechazado

Singleton para `FabricaGPS`: estado global que impide inyectar `GpsOperadorA(fallas=2)` en pruebas. Se inyecta la dependencia en su lugar.
