# Comparación — RutaSIT Arequipa (Lab 06)

## 1. Vista dinámica C4 frente al diagrama de secuencia UML (Lab 05) — E4

La secuencia de `lab05/diagrama_secuencia.puml` conserva el detalle de implementación que la
vista dinámica omite: el `loop` de consulta periódica cada 10 s, los fragmentos `alt/else` con
sus ramas (bus fuera de servicio, telemetría obsoleta, `EN_ESPERA` sin ETA ni alerta), las guardas
numéricas (30 s de vigencia, 30 m de ruta, 15 m de paradero), los parámetros y retornos de cada
operación (`es_reciente`, `distancia_a`, `desde_bus`) y los mensajes internos del dominio.
El público también cambia: la secuencia UML sirve al equipo de desarrollo que implementa y prueba
el contrato de cada operación; la vista dinámica sirve a arquitectos y revisores técnicos que
necesitan entender de un vistazo cómo colaboran los contenedores y componentes en el escenario
crítico (HU-06) sin entrar al detalle de las operaciones.

### Coherencia paso a paso con la secuencia del Laboratorio 05

| Paso | Vista dinámica | Origen en el Laboratorio 05 |
|---|---|---|
| 1 | GPS → Presentación: «Envía la posición de cada unidad cada 10 s» | `diagrama_actividades.puml`: captura y `procesar_telemetria` (RF-01) |
| 2 | Pasajero → Presentación: «Consulta la ubicación y el ETA de su bus» | Secuencia: `Pasajero -> API: consultar_seguimiento(...)` |
| 3 | Presentación → Aplicación: «Delega consultar_seguimiento(bus, paradero)» | Secuencia: `API -> Controller` y `Controller -> Service` |
| 4 | Infraestructura → BD: «Obtiene bus, ruta, paradero y la última posición GPS» | Secuencia: `Service -> Repo` (`obtener_bus/ruta/paradero`) y `Service -> GPS` (`obtener_ultima_ubicacion`) |
| 5 | Aplicación → Dominio: «Aplica reglas: vigencia ≤ 30 s, geocerca 30 m / 15 m y ETA» | Secuencia: `Bus.actualizar_ubicacion`, `es_reciente`, `actualizar_estado_por_ubicacion`, `detectar_desvio`, `calcular_eta` |
| 6 | Aplicación → Cola: «Encola la alerta de desvío para su envío asíncrono» | Secuencia: `AlertaDesvio.desde_bus` y `Notificador.notificar(alerta)` («aceptada para envío asíncrono») |
| 7 | Worker → Cola: «Consume posiciones y alertas» | `despliegue.py`: `app >> encola >> cache >> worker` (Worker ETA/alertas) |
| 8 | Worker → BD: «Actualiza el estado del bus y registra la alerta» | Persistencia del estado y del historial de alertas (RF-07) |
| 9 | Operador → Presentación: «Consulta el panel de flota y el historial de alertas» | `drivers.md`: RF-04, RF-06 y RF-07 (panel del operador) |

Cada paso usa una relación ya existente en `workspace.dsl`; la vista no introduce relaciones nuevas.
