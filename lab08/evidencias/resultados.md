# Resultados ejecutados — E2/E4

Generado con `python -m fitness.experimentos`. Tiempos simulados; semilla 7 en las tablas.
El JSON contiene las tres semillas y todos los casos. No son mediciones de producción.

## Ingesta: 1200 buses, 300 s, 36 000 eventos

| Configuración | Llegadas | p95 extremo a extremo (s) | % ≤15 s | Eventos fuera de cierre+15 s por minuto | Pendientes a 300 s |
|---|---|---:|---:|---|---:|
| base | fases | 95.166 | 11.24 | [717, 2467, 4243, 5960, 7200] | 8700 |
| base | ráfaga | 99.919 | 6.30 | [717, 2467, 4242, 5960, 7200] | 8700 |
| optimizada | fases | 4.212 | 100.00 | [0, 0, 0, 0, 0] | 0 |
| optimizada | ráfaga | 7.616 | 100.00 | [0, 0, 0, 0, 0] | 0 |

## Consultas: p95 (ms), 300 s por ensayo

| Configuración | Aciertos | 13,89 req/s | 69,44 req/s (pico ×5) |
|---|---:|---:|---:|
| base | 0% | 75155.670 | 1496233.391 |
| indice | 0% | 142.522 | 261.195 |
| solo_cache | 80% | 318.458 | 91843.044 |
| indice_cache | 80% | 128.900 | 130.788 |
| indice_cache | 0% | 142.757 | 256.663 |

## Mapas: caída de 1200 s durante 1800 consultas

| Configuración | Pantallas vacías | Llamadas durante caída | Recuperación (s) |
|---|---:|---:|---:|
| base | 1200 | 1200 | 0 |
| reintentos | 1200 | 3600 | 0 |
| fallback | 0 | 1200 | 0 |
| breaker | 0 | 42 | 2 |

## Sensibilidad: multiplicar tiempos de servicio

| Factor | Ingesta sincronizada p95 (s) | Consultas ×5, caché fría p95 (ms) |
|---|---:|---:|
| 1 | 7.616 | 256.663 |
| 1.5 | 9.325 | 86743.132 |
| 2 | 11.033 | 210726.426 |
| 3 | 33.153 | 458693.014 |
