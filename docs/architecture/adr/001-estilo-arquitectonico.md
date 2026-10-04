# ADR-001: Estilo arquitectónico — monolito modular

## Estado
Aceptado

## Fecha
2026-10-04

## Decisores
Grupo B: Layme Salas Rodrigo Fabricio, Auccacusi Conde Brayan Carlos,
Castillo Lazo Rodrigo Zarun.

## Contexto
RutaSIT Arequipa (caso N.º 6): 300 buses envían posición cada 10 s (QA-01,
ETA ≤ 15 s); MVP en 1 mes (R-01); equipo de 3 sin DevOps (R-02); un VPS (R-03).
Ver `../drivers.md` y `../matriz-decision.md`.

## Alternativas consideradas
1. **A. Monolito en capas** (4,10): un proceso, sin cola; simple pero ingesta
   acoplada a la API.
2. **B. Microservicios con broker** (3,05): escala independiente, pero exige
   Kafka/K8s y multiplica despliegues.
3. **C. Monolito modular + cola ligera Redis** (4,20): un despliegue Django con
   módulos (Ingesta, Flota, ETA, Alertas, Rutas) y cola Redis.

## Decisión
Usaremos el **monolito modular con cola ligera Redis** en un único VPS.

## Consecuencias
- Positiva: cumple QA-01 con 30 eventos/s sin infraestructura distribuida;
  respeta R-01/R-02/R-03; módulos extraíbles si la flota supera 600 buses.
- Negativa: el VPS único es punto simple de falla; se mitiga con última
  posición conocida, reintentos idempotentes y monitoreo (QA-02).
