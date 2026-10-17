# Revisión C4 — RutaSIT Arequipa (Lab 06, E7)

Proceso: el equipo aplicó la lista de revisión de la Tabla 3 (generales, elementos y relaciones)
a las cinco vistas; después, un auditor IA (Prompt IA 2 de la guía) revisó los `.puml` exportados
y las imágenes, y el equipo verificó cada hallazgo contra `workspace.dsl` y las fuentes de los
Laboratorios 04 y 05 antes de aceptarlo o descartarlo. Evidencia citada del modelo
(`workspace.dsl`), de los exports (`export/*.puml`) y de las imágenes (`img/`).

## 1. Lista de revisión aplicada a las cinco vistas

### Vista de contexto (nivel 1)

| Grupo | Pregunta | ¿Cumple? | Evidencia |
|---|---|---|---|
| General | ¿Título, tipo de diagrama y alcance? | Sí | `title ... "System Context View: RutaSIT Arequipa"` y subtítulo «Nivel 1: RutaSIT, sus usuarios y los sistemas externos.» |
| General | ¿Leyenda? | Sí | `SHOW_LEGEND(true)` (persona y sistema). Los externos llevan la etiqueta «Externo» en el modelo (ver hallazgo 1). |
| Elementos | ¿Nombre, tipo y descripción de cada elemento? | Sí | `Person(Pasajero ...)`, `Person(Operador ...)`, `System(RutaSITArequipa ...)`, `System(RastreadorGPSdelosbuses ...)`, `System(MapasabiertosOSM ...)`. |
| Elementos | ¿Acrónimos entendibles? | Sí (corregido en esta revisión) | «ETA (tiempo estimado de llegada)» y «SIT (Sistema Integrado de Transporte)»: expansiones tomadas de `docs/architecture/drivers.md`. |
| Relaciones | ¿Etiqueta con intención, dirección y protocolo cuando aplica? | Sí | `Rel(..., "Transmite la posición de cada unidad cada 10 s", $techn="HTTPS/JSON")` y `Rel(..., "Solicita tiles y geometría del mapa", $techn="HTTPS")`; con las personas no aplica protocolo en el nivel 1. |

### Vista de contenedores (nivel 2)

| Grupo | Pregunta | ¿Cumple? | Evidencia |
|---|---|---|---|
| General | ¿Título, tipo de diagrama y alcance? | Sí | `"Container View: RutaSIT Arequipa"` y subtítulo «Nivel 2: contenedores del sistema y su tecnología.» |
| General | ¿Leyenda? | Sí | `SHOW_LEGEND(true)` con límite discontinuo para el sistema. |
| Elementos | ¿Cada contenedor con nombre, tipo y tecnología? | Sí | `Container(... "API RutaSIT" $techn="Python 3.11 / Django")`, `Container(... "Worker ETA/Alertas" $techn="Celery")`, `ContainerQueue(... "Cola y caché" $techn="Redis")`, `ContainerDb(... "Base de datos" $techn="PostgreSQL")`; ninguno se llama «Docker», «servidor» ni «nube». |
| Relaciones | ¿Etiqueta y protocolo? | Sí | `Rel(... "Encola posiciones y alertas" $techn="Redis protocol")`, `Rel(... "Lee y escribe rutas, paraderos, estado y alertas" $techn="SQL/TCP")`, `Rel(... "Consulta la ubicación y el ETA de su bus" $techn="HTTPS/JSON")`. |

### Vista de componentes (nivel 3, contenedor API RutaSIT)

| Grupo | Pregunta | ¿Cumple? | Evidencia |
|---|---|---|---|
| General | ¿Título, tipo de diagrama y alcance? | Sí | `"Component View: RutaSIT Arequipa - API RutaSIT"` y subtítulo «Nivel 3: capas internas del monolito modular, coherentes con diagrama_paquetes.puml (Lab 05).» |
| Elementos | ¿Componentes coherentes con el Lab 05, con tecnología? | Sí | Presentación, Aplicación, Dominio, Infraestructura y Compartido (`$techn="Python 3.11"`; Presentación: «Python 3.11 / Django»), las cinco capas de `lab05/diagrama_paquetes.puml`, sin ciclos. |
| Relaciones | ¿Intención clara y tecnología solo donde aplica? | Sí | Internas en proceso sin tecnología (`"Invoca consultas y casos de uso"`); hacia contenedores/actores con tecnología (`"Redis protocol"`, `"SQL/TCP"`, `"HTTPS/JSON"`). |

### Vista dinámica (HU-06, extremo a extremo)

| Grupo | Pregunta | ¿Cumple? | Evidencia |
|---|---|---|---|
| General | ¿Título, tipo de diagrama y alcance? | Sí (corregido en esta revisión) | Subtítulo «Dinámico de extremo a extremo (HU-06): ingesta GPS, consulta del pasajero, alerta de desvío y panel del operador.» |
| Elementos | ¿Participantes tipados y definidos una sola vez? | Sí | Pasos numerados 1–9; el PNG dibuja cada elemento una sola vez (la repetición de declaraciones en el `.puml` es estructura del exportador; ver hallazgo 4). |
| Relaciones | ¿Orden, etiqueta y tecnología? | Sí | Pasos sobre relaciones existentes en el modelo; `"1: ..." $techn="HTTPS/JSON"`, `"4: ..." y "8: ..." $techn="SQL/TCP"`, `"6: ..." y "7: ..." $techn="Redis protocol"`; los pasos internos 3 y 5 no llevan tecnología. |
| Relaciones | ¿El flujo cubre el escenario crítico? | Sí | Coherencia paso a paso con la secuencia del Lab 05 documentada en `comparacion.md` (§1); ver hallazgo 5 (falso positivo). |

### Vista de despliegue (Producción)

| Grupo | Pregunta | ¿Cumple? | Evidencia |
|---|---|---|---|
| General | ¿Título, tipo de diagrama y alcance? | Sí | `"Deployment View: RutaSIT Arequipa - Producción"` y subtítulo «Despliegue en producción del MVP: VPS único (R-03) y rastreadores GPS de los buses.» |
| General | ¿Leyenda? | Sí | `SHOW_LEGEND(true)` con nodo, sistema y contenedor. |
| Elementos | ¿Nodos anidados con tipo y descripción? | Sí | `Deployment_Node(... "Bus del SIT (300 unidades)" ...) > "Rastreador GPS"`; `Deployment_Node(..., "VPS único (R-03)", $type="Ubuntu 24.04 LTS, 2 vCPU, 4 GB RAM")`, coherente con R-03 (bajo costo). |
| Elementos | ¿Instancias de **todos** los contenedores? | Sí | `containerInstance rutasit.app`, `rutasit.worker`, `rutasit.cache` y `rutasit.db` en el nodo de la VPS (véase también el PNG). |
| Relaciones | ¿Etiqueta, dirección y protocolo? | Sí | `"Envía la posición de cada unidad cada 10 s" $techn="HTTPS/JSON"`, `"Guarda posiciones, estado del bus y alertas" $techn="SQL/TCP"`, `"Consume posiciones y alertas" $techn="Redis protocol"`. |

## 2. Hallazgos del auditor IA y verificación del equipo

| Vista | Hallazgo del auditor IA | Verificación del equipo |
|---|---|---|
| Contexto (y demás) | Los sistemas externos no se distinguen en el export (`$tags=""`; la leyenda no muestra «external»). | **Correcto (limitación aceptada y documentada)**: el modelo sí les asigna la etiqueta «Externo» y el export Mermaid la refleja en gris; el formato `plantuml/c4plantuml` de la CLI no traduce etiquetas ni estilos (se comprobó también con una etiqueta `External`). No se editan los exports a mano (fuente única). |
| Contexto y Despliegue | Faltan expansiones de acrónimos (ETA, SIT, VPS). | **Correcto, corregido**: ETA y SIT se expanden con las definiciones de `drivers.md`; VPS se explica en la descripción del nodo. R-03 y HU-06 se mantienen como códigos de trazabilidad de los laboratorios anteriores. |
| Dinámica | El título no cubre los pasos 1 y 9 (ingesta periódica y operador). | **Correcto, corregido**: la descripción declara ahora el alcance de extremo a extremo; no se quitaron pasos porque la alerta asíncrona y el panel del operador son parte deliberada del escenario. |
| Dinámica | Declaraciones duplicadas en el `.puml` (bloque de líneas 37–42). | **Falso positivo**: es la estructura normal del exportador para elementos dentro y fuera del límite; el PNG dibuja cada elemento una sola vez y el archivo se regenera desde el modelo (no se edita a mano). |
| Dinámica | Paso 4 sin un paso previo «Aplicación → Infraestructura». | **Falso positivo**: patrón puertos/adaptadores; la secuencia del Lab 05 llama `Service -> Repo: obtener_bus/ruta/paradero` y el repositorio **es** el adaptador de infraestructura: no falta ningún paso. |
| Todas | ¿Falta un contenedor cliente (web o móvil)? | **Decisión de alcance verificada**: los Laboratorios 04 y 05 no definen una aplicación cliente propia; el navegador es software del usuario y el API «sirve el mapa del pasajero y el panel del operador» (descripción del contenedor). Queda registrado en la bitácora. |
| Contenedores, Componentes y Despliegue | Tecnologías, protocolos, nodos e instancias. | **Correcto (cumple)**: p. ej. `ContainerQueue(..., $techn="Redis")` con `Redis protocol` en sus relaciones, `SQL/TCP` hacia la base de datos, y el nodo VPS con SO y tamaño (R-03). |

Falsos positivos confirmados por el equipo: los dos marcados arriba (duplicación del `.puml` y
paso 4 del flujo); ambos se descartaron con la evidencia citada.

## 3. Correcciones aplicadas en esta revisión

- Descripciones del modelo ampliadas: «ETA (tiempo estimado de llegada)», «SIT (Sistema Integrado
  de Transporte)» y VPS explicado en el nodo de despliegue.
- Vista dinámica: descripción ajustada al alcance real (extremo a extremo, 9 pasos).
- `inventario.md`: la fila del despliegue ya no menciona «dispositivos de usuario»; se agregó la
  nota de alcance (Structurizr descarta los nodos sin instancias y ningún contenedor de RutaSIT
  se ejecuta en los dispositivos).
- Re-exportación a C4-PlantUML y Mermaid y regeneración de los seis PNG tras las correcciones.
