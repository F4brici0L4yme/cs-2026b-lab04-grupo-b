# E1 — Escenarios y árbol de utilidad

Fuente: [entradas](../entradas.md), drivers del Lab 04 y crecimiento de la tabla 11
de la guía 08. H/M/L significan alta/media/baja. Cada prioridad es una propuesta
de trabajo revisable por el grupo; la dificultad considera el prototipo y las pruebas.

| ID / atributo / prioridad | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida |
|---|---|---|---|---|---|---|
| QA-01 Rendimiento (H,H) | 1200 buses | Una posición por bus cada 10 s | Hora punta; fases distribuidas y ráfagas sincronizadas | Ingesta + worker ETA | Procesar telemetría y publicar ETA consultable | p95 captura→consulta ≤15 s; 100% de eventos del intervalo de captura de 60 s completados antes de su cierre +15 s |
| QA-02 Disponibilidad (H,M) | Proveedor de mapas | Caída de 20 min | Ingesta y API disponibles | Vista del pasajero + adaptador mapas | Mantener estado textual y advertir degradación; recuperar mapa | 0 respuestas sin estado; recuperación ≤300 s; objetivo de sondeo ≤30 s |
| QA-03 Rendimiento/escalabilidad (H,H) | Expansión de flota | Pasar 300→600→1200 buses | Mismo VPS; un mes | API, worker, Redis y BD | Absorber carga sin cambiar el estilo | p95 ETA ≤15 s en las tres cargas; CPU <70% requiere medición real pendiente |
| QA-04 Rendimiento (H,H) | Pasajeros | 50 000 consultas en una hora; concentración ×5 | Caché caliente y fría | API y almacenamiento de ETA | Responder la consulta sin recalcular geometría por petición | p95 respuesta ≤2000 ms a 13,89 y 69,44 req/s |
| QA-05 Seguridad (M,L) | Cliente público | Solicitar 100 respuestas de seguimiento | Operación normal y degradada | DTO público | Entregar datos de unidad sin datos personales de conductor | 0 campos de nombre, DNI, teléfono u otro identificador personal; lista permitida exacta en 100 respuestas |
| QA-06 Modificabilidad (M,L) | Desarrollador | Agregar algoritmo ETA nocturno | Desarrollo; registros Strategy/Factory del Lab 07 | Fábrica de ETA | Registrar nueva estrategia conservando servicio | 0 líneas cambiadas en `ServicioSeguimiento`; pasa prueba de extensión del Lab 07 |
| QA-07 Disponibilidad/frescura (H,M) | Bus sin señal o mensaje retrasado | Lectura supera 30 s o llega fuera de orden | Caché activa, mapa disponible o caído | Repositorio, caché, caso de uso | Marcar SIN_SEÑAL sin ETA actual; no retroceder la lectura guardada | 0 respuestas ACTUAL con edad >30 s o negativa; 0 reemplazos por evento duplicado/antiguo |

## Priorización y corrección argumentada

QA-01 y QA-04 son (H,H): el aumento de escritura y lectura afecta directamente
la utilidad para el pasajero. QA-03 rastrea el crecimiento del Lab 04 y comparte
evidencia con QA-01; no se cuenta como una iteración diferente.
QA-02 y QA-07 son (H,M): conservar información útil exige controlar dependencias
y vigencia, sin una plataforma distribuida nueva.

**Corrección de la propuesta inicial de IA:** clasificar QA-05 como (H,H) por
el crecimiento de flota sobredimensiona este escenario concreto. R-04 y HU-06
ya excluyen datos identificativos del conductor, y el DTO permite una prueba
de lista cerrada. Se propone **(M,L)** para este escenario. Esto no reduce la
importancia de autenticación ni demuestra cumplimiento integral de la Ley 29733.
El equipo debe confirmar esta corrección en su revisión del entregable.

QA-06 es (M,L): la extensión ya tiene una prueba en Lab 07; no requiere cambiar
el estilo ni motivar una cuarta iteración.

## Selección ADD

1. Iteración 1: QA-01 (y trazabilidad de QA-03), mayor prioridad técnica.
2. Iteración 2: QA-04, respetando QA-07 y el DTO de QA-05.
3. Iteración 3: QA-02, respetando QA-07 durante la degradación.

El árbol editable está en `arbol.dot`; `arbol.png` y `arbol.svg` se generan con Graphviz.
