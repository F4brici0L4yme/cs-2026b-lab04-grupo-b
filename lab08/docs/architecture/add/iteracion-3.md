# E4 — Iteración ADD 3: disponibilidad de la vista ante caída de mapas

## 1. Revisar entradas

QA-02 (H,M) procede del Lab 04: cero pantallas vacías y recuperación ≤5 min.
QA-07 limita la vigencia de la información. El análisis ATAM propio detecta
R5: fallas externas y reintentos pueden consumir recursos que necesita la API.
La evaluación externa E3 sigue pendiente; no se atribuyen hallazgos a otro grupo.

## 2. Elegir objetivo

Ante 20 minutos sin mapas: ninguna respuesta carece de estado textual,
recuperación ≤300 s (objetivo de sondeo 30 s), y al menos 5 veces menos llamadas
al proveedor caído que con tres reintentos por solicitud.

## 3. Elegir elemento a refinar

Puerto de mapas y vista del pasajero, manteniendo separada la consulta de ETA.
No se aplica circuit breaker a una captura GPS local ni se inventa un sistema de pagos.

## 4. Elegir conceptos de diseño

| Candidato | Mejora | Trade-off / costo | Decisión |
|---|---|---|---|
| Tres reintentos inmediatos | Puede tolerar fallas transitorias | Triplica llamadas durante caída sostenida; bloquea consulta | Rechazado para la caída de 20 min |
| Solo vista textual alternativa | Mantiene información útil | Sigue llamando al proveedor caído en cada petición | Necesario pero insuficiente para protección |
| Circuit breaker + vista textual | Falla rápida y reduce llamadas; mantiene ETA/estado | Puede retrasar recuperación hasta el próximo sondeo; estado por proceso | Seleccionado |
| Segundo proveedor de mapas | Redundancia externa | Costos, compatibilidad y políticas/licencias; no probados | Diferido hasta justificar servicio pagado |

## 5. Instanciar responsabilidades e interfaces

`ConCircuitBreaker` implementa `Mapas` por composición, como el Decorator de
reintentos del Lab 07. Abre tras tres fallas consecutivas; espera 30 s; sondea
en SEMIABIERTO; éxito reinicia contador y cierra; error vuelve a abrir.
`VistaSeguimiento` captura fallas de conexión/timeout y devuelve estado más aviso.
No inventa ETA si no hay dato o si la fuente supera 30 s.

El adaptador HTTP de producción deberá imponer timeout de transporte (p. ej.
500 ms), bloquear sondeos concurrentes y tratar HTTP 5xx/429 apropiadamente.
El prototipo es **secuencial**, con excepción de timeout inyectada; no mide demora
de sockets ni coordinación entre procesos. Los reintentos idempotentes GPS de
ADR-003 permanecen en otro flujo. Alertar por >5% de fallas durante 2 min sigue
siendo requisito de monitoreo del Lab 04, no una instalación Grafana realizada aquí.

## 6. Esbozar vistas y registrar decisiones

[ADR-008](../adr/008-disponibilidad-mapas.md), componente de infraestructura y
relación API→Mapas anotados QA-02. La vista textual reside en la API, sin nuevo
contenedor ni dependencia de disponibilidad del proveedor para obtener el ETA.

## 7. Analizar con evidencia

`fitness/disponibilidad.py` ejecuta código del prototipo. 1800 consultas, una por
segundo; proveedor falla en [300,1500); GPS sigue actualizándose cada 10 s.
La lectura se consulta en todas las respuestas degradadas. Reloj virtual sin
esperas reales: experimento determinista de fallo, no disponibilidad anual.

| Variante | Pantallas vacías | Llamadas durante caída | Recuperación |
|---|---:|---:|---:|
| Acoplamiento directo | 1200 | 1200 | 0 s |
| Tres reintentos | 1200 | 3600 | 0 s |
| Solo fallback | 0 | 1200 | 0 s |
| Breaker + fallback | 0 | 42 | 2 s |

![Disponibilidad](../../../evidencias/disponibilidad.png)

3600/42 = **85,71 veces menos llamadas**. FF-05 verifica los umbrales; pruebas
adicionales ejercitan reapertura y cierre, señal vencida y ausencia de lectura.
La pérdida temporal del mapa se informa: cero pantallas vacías no significa
cero degradación (se registran 1202 respuestas degradadas).

**Conclusión:** QA-02 cumple en la falla inyectada y se mitiga R5 bajo ejecución
secuencial. El único VPS sigue siendo un punto de falla (R2); esta táctica no
pretende resolver su caída ni demostrar durabilidad de Redis.
