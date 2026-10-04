# ADR-003: Comunicación — REST síncrono al borde y cola Redis interna

## Estado
Aceptado

## Fecha
2026-10-04

## Decisores
Grupo B: Layme Salas Rodrigo Fabricio, Auccacusi Conde Brayan Carlos,
Castillo Lazo Rodrigo Zarun.

## Contexto
Los buses envían posición cada 10 s por 3G/4G (R-05) y el pasajero exige
ETA ≤ 15 s (QA-01); el equipo evita operar brokers distribuidos (R-02/R-03).

## Alternativas consideradas
1. **REST síncrono de punta a punta**: simple, pero un pico de 300 buses
   bloquea la API y propaga la lentitud al ETA.
2. **Broker distribuido (Kafka)**: durable y escalable, pero sobredimensionado
   para 30 eventos/s y viola R-02/R-03.
3. **REST al borde + cola Redis interna**: el borde acepta rápido y encola;
   el worker calcula ETA/alertas de forma asíncrona.

## Decisión
Usaremos **REST al borde con cola Redis interna** y reintentos idempotentes.

## Consecuencias
- Positiva: desacopla ingesta de cálculo, absorbe picos y mantiene QA-01 con
  una sola pieza extra (Redis) en el VPS.
- Negativa: Redis en memoria exige límites de memoria y persistencia AOF;
  se mitiga con TTL, última posición conocida y monitoreo.
