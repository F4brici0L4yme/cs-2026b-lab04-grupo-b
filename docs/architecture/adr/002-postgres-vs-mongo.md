# ADR-002: Base de datos — PostgreSQL con esquemas por módulo

## Estado
Aceptado

## Fecha
2026-10-04

## Decisores
Grupo B: Layme Salas Rodrigo Fabricio, Auccacusi Conde Brayan Carlos,
Castillo Lazo Rodrigo Zarun.

## Contexto
Se necesita persistir posiciones GPS (alta escritura), rutas/paraderos y
estado de flota, con equipo que domina SQL (R-02), un VPS (R-03) y Ley
N.º 29733 (R-04). Requiere QA-01 (ingesta 30 eventos/s) y QA-03 (crecer a
600 buses sin rediseño).

## Alternativas consideradas
1. **PostgreSQL con un esquema por módulo**: relacional, conocido por el
   equipo, Timescale/índices espacio-temporales si hace falta; un solo motor.
2. **MongoDB/documental**: flexible para tracks GPS, pero sin experiencia en
   el equipo y agrega un motor más al VPS.

## Decisión
Usaremos **PostgreSQL con un esquema por módulo** y tablas de series
temporales para posiciones.

## Consecuencias
- Positiva: un solo motor en el VPS, transacciones para rutas/ETA, equipo
  productivo desde el día 1 (R-01/R-02/R-03).
- Negativa: picos de escritura exigen índices y purga de posiciones antiguas;
  se mitiga con particionado por tiempo y TTL.
