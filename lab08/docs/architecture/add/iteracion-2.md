# E4 — Iteración ADD 2: consultas de ETA y frescura

## 1. Revisar entradas

QA-04 (H,H), QA-07 (H,M), HU-06, PostgreSQL de ADR-002 y Decorator de ADR-005.
La iteración 1 reduce trabajo del worker; ahora se estudia la lectura sin
recalcular geometría por cada pasajero. El DTO conserva R-04 (QA-05).

## 2. Elegir objetivo

p95 consulta ≤2000 ms a 13,89 req/s y pico de 69,44 req/s, incluso con caché fría.
No mostrar como actual una fuente de más de 30 s. Las 50 000 consultas no se
interpretan como 50 000 conexiones simultáneas (supuesto S-01).

## 3. Elegir elemento a refinar

Read model de ETA en PostgreSQL, puerto de lectura de aplicación y caché Redis.

## 4. Elegir conceptos de diseño

| Candidato | Mejora | Trade-off / costo | Decisión |
|---|---|---|---|
| Solo caché, sin mejorar consulta de respaldo | Baja latencia con aciertos altos | Dependencia de popularidad, TTL y arranque; costo bajo | Rechazado como solución suficiente: falla con caché fría y en pico |
| Último ETA por bus/paradero + índice compuesto | Reduce búsqueda, evita recorrer historial | Más escrituras por actualización y espacio de índice; esfuerzo medio | Seleccionado como base |
| Índice + caché TTL 2 s acotada | Reduce lecturas repetidas y da margen | Hasta 2 s de antigüedad adicional, RAM e invalidación; esfuerzo medio | Seleccionado como margen, sin exigir tasa de aciertos para cumplir |
| Réplica de lectura en otro VPS | Aislamiento y capacidad | Costo extra, retraso de replicación y operación | Rechazado bajo R-03; revisar si medición real lo exige |

## 5. Instanciar responsabilidades e interfaces

Worker actualiza un ETA por `(bus_id, paradero_id)`. Tabla objetivo con clave
compuesta y timestamp de captura; el historial sigue aparte. API consulta
`RepositorioETA`, decorado con `ConCacheETA`; cada respuesta pasa por la regla
`LecturaETA.vigente`, incluso si el TTL no venció. Clave de caché incluye bus y
paradero; capacidad máxima del prototipo 2400 entradas, expulsión LRU.
Ese número es un límite experimental, no el total de pares bus/paradero del SIT.

Una ausencia no se cachea. La respuesta SIN_DATOS/SIN_SEÑAL permite presentar
información honesta. Se usan únicamente datos públicos de unidad en el DTO;
FF-07 verifica la lista exacta de campos. El ejemplo de DDL está en
`prototipo-read-model.sql`; es diseño para PostgreSQL, no un benchmark SQL.

## 6. Esbozar vistas y registrar decisiones

[ADR-007](../adr/007-consultas-eta.md); relaciones de lectura API→Redis/BD y
escritura Worker→Redis/BD en el C4 con trazabilidad QA-04/QA-07.

## 7. Analizar con evidencia

`simular_consultas`: llegadas Poisson, 300 s, dos servidores, servicio lognormal
sigma 0,35; medias hipotéticas 180 ms base, 25 ms con índice/read model y 3 ms
con acierto. Se añaden 100 ms de transporte/serialización. Los tiempos no están
calibrados con PostgreSQL; 80% de aciertos es un escenario exploratorio, no una
tasa medida ni garantizada con TTL 2 s. También se prueba 0% y 20%.

| Configuración | p95 normal | p95 pico ×5 |
|---|---:|---:|
| Base | 75 155,670 ms | 1 496 233,391 ms |
| Solo índice/read model | 142,522 ms | 261,195 ms |
| Solo caché, 80% aciertos | 318,458 ms | 91 843,044 ms |
| Índice + caché, 80% | 128,900 ms | 130,788 ms |
| Índice + caché, 0% | 142,757 ms | 256,663 ms |

![Consultas](../../../evidencias/consultas.png)

La semilla 7 se muestra arriba; JSON y FF-04 cubren tres semillas. El ensayo de
QA-07 accede a una lectura a los 29,5 s y repite a los 30,5 s: el TTL aún tiene
tiempo, pero el ETA se retira por edad de fuente. También hay pruebas de claves
distintas, expiración exacta, desorden, ausencia y límite de entradas.

**Sensibilidad crítica:** a 37,5 ms de servicio (25 ms ×1,5), dos servidores solo
ofrecen 53,33 req/s <69,44. Con caché fría, p95 alcanza 86 743,132 ms. No basta
afirmar que «el índice resuelve todo»: R1 exige perfilado de consulta real y prueba
mixta. Se adopta como diseño condicionado a esa validación.

**Conclusión:** QA-04 cumple en los parámetros ensayados; QA-07 se verifica en el
prototipo. El riesgo de ETA obsoleto R3 se mitiga sin atribuir al TTL el poder de
rejuvenecer una captura. La ventaja de caché es carga, no una garantía de frescura.
