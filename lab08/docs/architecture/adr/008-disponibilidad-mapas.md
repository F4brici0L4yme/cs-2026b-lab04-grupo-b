# ADR-008: Circuit breaker y estado textual ante caída de mapas

## Estado
Seleccionado y verificado en prototipo secuencial; pendiente ratificación del grupo
y adaptación HTTP concurrente. Conserva presupuesto y contenedores de ADR-001.

## Fecha
2026-10-27

## Decisores
Grupo B: Layme Salas Rodrigo Fabricio, Auccacusi Conde Brayan Carlos y
Castillo Lazo Rodrigo Zarun. Propuesta asistida para revisión del equipo.

## Contexto
QA-02 y riesgo R5: proveedor de mapas cae 20 min; la información de seguimiento
debe continuar, sin tormenta de reintentos. QA-07 impide presentar fuentes
vencidas como actuales. Ver [iteración 3](../add/iteracion-3.md).

## Alternativas consideradas
1. Tres reintentos inmediatos: triplica llamadas a proveedor caído.
2. Solo fallback textual: continuidad sin protección de carga externa.
3. Circuit breaker más fallback: protección y continuidad con posible retraso
   en recuperación.
4. Segundo proveedor: contratación, costos y políticas de uso sin validar.

## Decisión
Decorator sobre puerto Mapas: abre tras 3 errores, sondea luego de 30 s y cierra
al primer éxito. Consultar ETA independientemente del mapa; devolver estado
textual y aviso cuando el mapa falla. Si no hay lectura válida, indicar SIN_DATOS
o SIN_SEÑAL, sin inventar un ETA actual.

## Evidencia
1800 solicitudes; caída inyectada de 1200 s: pantallas vacías **1200→0**;
llamadas durante caída **3600 (reintentos)→42 (breaker)**; recuperación **2 s**.
FF-05 más pruebas de reapertura/cierre verifican el código, incluyendo casos sin
lectura y con señal vencida. No son estadísticas anuales de disponibilidad.

## Consecuencias
- Positiva: menos llamadas inútiles y estado disponible durante la caída externa.
- Negativa: hasta 30 s adicionales para sondear recuperación; se pierde mapa
  temporalmente aunque el texto siga disponible.
- Trade-off: protección del proveedor frente a recuperación inmediata.
- El estado del breaker es por instancia, secuencial. Para múltiples procesos
  se necesitan bloqueo de sondeo, límites globales y timeout real del adaptador.
- No mitiga una caída del propio VPS (R2), ni pérdida de posiciones en Redis (R4).
