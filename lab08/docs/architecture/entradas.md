# Entradas de ADD — continuidad con Labs 04–07

## Contexto y alcance

Caso 6, RutaSIT Arequipa, Grupo B. La guía 08 exige pasar de 300 a **1200 buses**
y atender **50 000 consultas de ETA en hora punta**, manteniendo un mes de adaptación,
tres desarrolladores Python/Django/JavaScript y un único VPS de bajo costo.
No se inventa un presupuesto monetario: R-03 del grupo no fija una cifra.

| Entrada | Archivo original desde la raíz del repositorio | Uso en Lab 08 |
|---|---|---|
| Drivers, RF-01 a RF-07, QA-01 a QA-03, R-01 a R-05 | `docs/architecture/drivers.md` | Escenarios de seis partes y restricciones |
| Estilo monolito modular | `docs/architecture/adr/001-estilo-arquitectonico.md` | Se conserva; cambiarlo requiere evidencia |
| PostgreSQL, esquemas por módulo | `docs/architecture/adr/002-postgres-vs-mongo.md` | Read model de ETA e índices candidatos |
| REST, cola Redis, IDs estables, AOF | `docs/architecture/adr/003-rest-vs-cola.md` | Ingesta asíncrona e idempotencia |
| HU-06; vigencia GPS de 30 s | `lab05/historia.md` | No presentar ETA obsoleto como actual |
| Capas y puertos | `lab05/diagrama_paquetes.puml` | Contratos de import-linter |
| API, worker, Redis, PostgreSQL | `lab06/docs/architecture/c4/workspace.dsl` | Modelo C4 de partida |
| Patrones y métricas | `lab07/docs/architecture/adr/005-patrones-de-diseno.md` | Strategy, Adapter y Decorator como puntos de extensión |
| Código de referencia | `lab07/src/rutasit/` | Reutilización conceptual y regresión de pruebas |

## Qué cambia y qué significa cada medida

- 300/10 = 30 eventos/s; 600/10 = 60; 1200/10 = **120 eventos/s**.
- Hipótesis S-01: las 50 000 consultas ocurren en una ventana de **una hora**:
  13,89 req/s. La guía no precisa duración/distribución. El Lab 04 identifica
  6:30–8:30 como franja punta; si se repartieran en dos horas serían 6,94 req/s.
  Se elige una hora conservadoramente y un ensayo de concentración ×5 (69,44 req/s).
  Ese ×5 es un ensayo de estrés, no una predicción ni una carga constante de 50 000/h.
- QA-01 mide captura GPS → disponibilidad del ETA consultado, p95 ≤15 s.
  No es el valor predicho de minutos de llegada ni el tiempo de respuesta HTTP.
  El intervalo de muestreo de 10 s es anterior a la captura y no se suma a esta medida.
- QA-04 agrega un presupuesto de respuesta de consulta p95 ≤2 s, **propuesto**
  para este laboratorio, no impuesto por el Lab 04.
- QA-03 conserva la intención de crecer sin rediseño y eleva el ensayo a 1200 buses.
  El objetivo original CPU <70% queda **sin verificar**: utilización de una cola
  no es CPU del VPS. No se presenta como cumplido por una simulación.

## Coherencia y límites de implementación

El C4 representa el diseño objetivo Django/Celery/Redis/PostgreSQL. El código
`lab08/src/rutasit8` es un **prototipo de puertos, caché y resiliencia en memoria**;
no despliega esos servicios. Su nombre evita mezclar los dos paquetes históricos
`rutasit` de Labs 05 y 07. Los experimentos de rendimiento modelan hipótesis;
los de disponibilidad ejecutan el Decorator y el caso de uso del prototipo.

El Lab 07 concentra construcción de adaptadores en `ServicioSeguimiento.__init__`
y en `FabricaGPS`. Por tanto, no sería correcto afirmar que ya tenía una regla
«solo arranque conoce adaptadores». Lab 08 explicita esa separación en `arranque.py`
como refinamiento de ADR-005, coherente con los puertos del Lab 05.

El único VPS del Lab 06 (2 vCPU/4 GB) continúa siendo una restricción de diseño.
Las colas de ingesta y consulta se simulan por separado; no prueban contención
simultánea de CPU, RAM, disco ni conexiones. Antes de producción se necesita una
prueba mixta sobre ese VPS. Esa limitación es el riesgo R1 del ATAM-lite.

## Organización

Los nuevos artefactos se guardan en `lab08/`, siguiendo los Labs 05–07.
`.importlinter`, `.github/workflows/fitness.yml` y la sección del README raíz son
los puntos de integración. La copia evolucionada del C4 está en
`lab08/docs/architecture/c4/workspace.dsl`, con referencia explícita al original.
