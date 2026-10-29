# ADR-006: Reducir trabajo por evento antes de distribuir la ingesta

## Estado
Seleccionado para el prototipo del Lab 08; ratificación del grupo y capacidad
real del VPS pendientes. Conserva ADR-001 y refina ADR-002/003.

## Fecha
2026-10-27

## Decisores
Grupo B: Layme Salas Rodrigo Fabricio, Auccacusi Conde Brayan Carlos y
Castillo Lazo Rodrigo Zarun. Propuesta elaborada con asistencia de IA para revisión.

## Contexto
QA-01/QA-03: 1200 buses generan 120 eventos/s, p95 actualización ≤15 s.
Un mes, tres desarrolladores, un VPS. La arquitectura anterior no contiene
mediciones que prueben esa capacidad. Ver [iteración 1](../add/iteracion-1.md).

## Alternativas consideradas
1. Reducir consultas repetidas y precargar geometría por versión: RAM y coherencia
   de configuración a cambio de menor tiempo de procesamiento.
2. Más workers: puede ayudar ante I/O, pero comparte recursos limitados.
3. Segundo VPS: costo adicional y distribución de responsabilidades.
4. Microservicios y broker distribuido: operación compleja para equipo/plazo.

## Decisión
Mantener monolito modular, REST al borde, cola Redis y worker ETA/Alertas.
Optimizar acceso a geometría y materializar último ETA; conservar historial,
IDs estables y procesamiento idempotente. Usar dos servidores lógicos en el
modelo para evaluar un objetivo de servicio de 6 ms/evento, que debe medirse
antes de desplegar. No asumir que cada worker equivale a un núcleo libre.

## Evidencia
36 000 eventos/300 s, ráfaga sincronizada, semilla 7: p95 base **99,919 s**;
optimizado **7,616 s**; 8700→0 eventos pendientes al cierre. FF-03 pasa para
semillas 7, 19 y 42. Al triplicar el servicio, p95 **33,153 s**: se invalida el
escenario. [Resultados y supuestos](../../../evidencias/resultados.md).

## Consecuencias
- Positiva: el modelo admite el crecimiento sin añadir un servicio pagado.
- Negativa: más memoria para geometría; su cambio exige invalidación por versión.
- Trade-off aceptado: CPU/I/O menor a cambio de memoria y sincronización de datos
  de referencia. La simulación no demuestra el ahorro real ni CPU <70%.
- Revisión obligatoria si la prueba mixta de VPS incumple QA-01, o aparece backlog
  persistente. R1/R4 permanecen en [ATAM-lite](../atam-lite.md).
