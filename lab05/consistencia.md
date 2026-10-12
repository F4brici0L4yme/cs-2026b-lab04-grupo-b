# Matriz de consistencia UML: RutaSIT, Lab 05

La matriz contrasta los cinco criterios solicitados con los diagramas y el esqueleto en `src/rutasit/`. La verificación del código se ejecuta con:

```bash
cd lab05
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Criterios C1-C5

| Criterio | Elementos contrastados | Verificación | Resultado |
|---|---|---|---|
| **C1: Clases vs. secuencia** | Cada mensaje de llamada de `diagrama_secuencia.puml` tiene una operación en `diagrama_clases.puml` y en el esqueleto. | Se cotejaron `consultar_seguimiento`, `obtener_bus/ruta/paradero`, `estado_actual`, `obtener_ultima_ubicacion`, `ahora`, `es_reciente`, `actualizar_ubicacion`, `actualizar_estado_por_ubicacion`, `detectar_desvio`, `esta_en_ruta`, `distancia_a`, `calcular_eta`, `desde_bus` y `notificar`. | **Cumple.** Los retornos describen valores de esas operaciones, no llamadas adicionales. |
| **C2: Secuencia vs. estados** | Estado que devuelve `Bus.actualizar_estado_por_ubicacion` en las ramas de telemetría reciente y desvío. | Se verificó que la operación aparece tanto en la secuencia como en las etiquetas de transición del diagrama de estados; las guardas usan los umbrales de 30 m para ruta y 15 m para paradero. | **Cumple.** `EN_ESPERA` solo sale mediante `iniciar_servicio()`; telemetría obsoleta y buses fuera de servicio no cambian de estado. |
| **C3: Estados vs. clases** | Enum `EstadoBus` y operaciones de `Bus`. | Se compararon los cinco valores de `EstadoBus` con los estados Mermaid y se asociaron `iniciar_servicio`, `actualizar_estado_por_ubicacion` y `retirar_servicio` con sus transiciones. | **Cumple.** No se usa un estado que no esté en la enumeración. |
| **C4: Actividades vs. secuencia** | Ingesta GPS, vigencia de coordenada, actualización del bus, ETA, geocerca y alerta. | La secuencia entra por `consultar_seguimiento` (consulta del pasajero) y la actividad por `procesar_telemetria` (evento del GPS); ambas validan vigencia y convergen en las mismas reglas de estado, ETA y alerta. La actividad muestra ETA y geocerca como tareas independientes en un `fork`. | **Cumple a nivel de flujo.** El esqueleto Python es síncrono; el `fork` expresa paralelismo posible, no un executor concurrente ya implementado. En `EN_ESPERA` se conserva la ubicación sin ETA ni alerta. |
| **C5: Paquetes vs. clases** | Ubicación de las clases de E1 en `presentacion`, `aplicacion`, `dominio`, `infraestructura` y `compartido`. | Se contrastaron los bloques del diagrama de paquetes con `diagrama_clases.puml` y los módulos Python. Las capas externas implementan/consumen puertos hacia dentro; no hay arco de retorno desde dominio a infraestructura o presentación. | **Cumple.** No se identifican dependencias cíclicas. El paquete Python raíz `rutasit` es un namespace técnico (no una sexta capa); `__init__.py` reexporta tipos públicos. El modelo evita almacenar PII del conductor: solo un identificador seudónimo y estado activo. |

## Falso positivo del análisis asistido

**FALSO POSITIVO:** Pyreverse representa `IGpsProvider`, `INotificadorAlerta` y otros `Protocol` como clases ordinarias y no dibuja las realizaciones de sus adaptadores. Un primer cotejo automatizado puede interpretarlo como “falta la interfaz” o “falta la realización”. Al revisar `puertos.py`, se confirma que son protocolos tipados y que `diagrama_clases.puml` declara explícitamente las realizaciones; la diferencia procede de la representación limitada de Pyreverse, no de una interfaz ausente en el diseño.

## Alcance de la comprobación

- Las pruebas unitarias cubren distancia, estados del bus, telemetría obsoleta y la emisión única de alerta al entrar en `DESVIADO`.
- La estimación ETA y la geocerca son esqueletos didácticos; no demuestran por sí solas el objetivo de p95 ≤ 15 s.
- La revisión final humana de los integrantes debe confirmar umbrales, nombres oficiales y criterios de aceptación antes de entregar.
