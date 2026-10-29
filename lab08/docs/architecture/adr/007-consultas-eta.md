# ADR-007: Read model indexado de ETA y caché breve con control de vigencia

## Estado
Seleccionado y prototipado para Lab 08; ratificación del grupo y perfilado SQL
pendientes. Refina ADR-002 y aplica Decorator de ADR-005.

## Fecha
2026-10-27

## Decisores
Grupo B: Layme Salas Rodrigo Fabricio, Auccacusi Conde Brayan Carlos y
Castillo Lazo Rodrigo Zarun. Propuesta asistida pendiente de revisión humana.

## Contexto
QA-04: 50 000 consultas/h como hipótesis y pico ×5; p95 ≤2 s. QA-07:
fuente GPS mayor a 30 s no puede mostrarse como actual. R-04: sin datos
personales de conductor. Ver [iteración 2](../add/iteracion-2.md).

## Alternativas consideradas
1. Solo caché: sensible a aciertos/arranque, no resuelve consulta lenta de respaldo.
2. Read model con índice compuesto: base rápida, más trabajo de escritura.
3. Índice y caché TTL 2 s: margen adicional a costo de memoria y desfase acotado.
4. Réplica de lectura externa: complejidad y costo no justificados por evidencia.

## Decisión
Consulta por clave `(bus_id, paradero_id)` al último ETA materializado, con índice
compuesto en PostgreSQL. Decorator `ConCacheETA` acotado, TTL ≤2 s. Verificar
timestamp de **captura** al responder; no renovar la edad del dato al cachearlo.
Exponer DTO de unidad sin identificadores personales. Crear dependencias concretas
en `arranque.py`, haciendo ejecutable el desacoplamiento del Lab 05 y ADR-005.

## Evidencia
Pico ×5, semilla 7: solo caché 80% → **91 843,044 ms**; índice+caché
80% → **130,788 ms**; con 0% → **256,663 ms**. Los tiempos son simulados.
FF-04 verifica tres semillas y 0/20/80% aciertos. FF-06 demuestra que una
captura de 30,5 s se rechaza aunque su TTL aún esté vigente; FF-07 restringe DTO.

## Consecuencias
- Positiva: lectura no recalcula todo el historial y la caché no es requisito
  para cumplir el presupuesto bajo las hipótesis ensayadas.
- Negativa: más escrituras/índices; puede servirse una versión anterior hasta
  2 s, dentro del presupuesto modelado. El cache hit real depende de popularidad.
- Trade-off: menor carga de lectura por frescura ligeramente menor y RAM extra.
- Riesgo R1: con servicio 50% más lento, caché fría y pico ×5 el p95 falla.
  Se exige EXPLAIN ANALYZE y carga mixta antes de afirmar capacidad de producción.
- El prototipo no sustituye aislamiento de transacciones ni durabilidad Redis/BD.
