# Bitácora de uso de IA — RutaSIT Arequipa

> **Regla de oro del curso:** la IA propone, el equipo decide y verifica.
> Los prompts completos están en [`prompts/`](prompts/) y se reproducen al final (Anexo).
> El nombre de la herramienta es referencial: ajústelo al asistente que realmente usaron.

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 29/09 | Claude | [`prompt-03-escenarios-calidad.md`](prompts/prompt-03-escenarios-calidad.md): redactar 3 escenarios de calidad de seis partes. | Escenarios redactados, pero con medidas vagas: «la app debe responder rápido» y «debe ser confiable». | Reemplazamos las medidas por valores numéricos y verificables tomados del caso: 300 buses, posición cada 10 s, p95 del ETA ≤ 15 s, recuperación ≤ 5 min, CPU < 70 % con 600 buses. | **Corregida** |
| 2 | 29/09 | Claude | [`prompt-01-alternativas.md`](prompts/prompt-01-alternativas.md): 3 alternativas de estilo con fortalezas, debilidades y riesgos. | Recomendó microservicios con Kubernetes y Kafka «por escalabilidad». | Cálculo: 300 × 1/10 s = 30 eventos/s, carga que un VPS y una cola ligera absorben. Microservicios viola R-02 (equipo sin DevOps) y R-03 (un VPS). Se conservaron como alternativas A y B en la matriz. | **Rechazada** |
| 3 | 30/09 | Claude | [`prompt-02-critica-adversarial.md`](prompts/prompt-02-critica-adversarial.md): abogado del diablo contra la alternativa elegida. | 5 riesgos: pérdida de eventos en picos, memoria de la cola, acoplamiento entre módulos, ETA sesgado (GPS impreciso) y caída del VPS único. Sugirió una base de datos de series temporales (InfluxDB). | Aceptamos las tácticas de cola con reintentos idempotentes y de «última posición conocida»; descartamos InfluxDB por costo y curva de aprendizaje (R-02/R-03). | **Corregida** |
| 4 | 30/09 | Claude | Verificación de datos: ¿la API de Google Maps da ETA de transporte público sin costo? | Afirmó que la API de Google Maps entrega ETA de transporte público «gratis e ilimitada». | Verificamos en la documentación oficial: requiere cuenta de facturación y tiene cuota gratuita limitada. Se adoptó un proveedor de mapas abiertas (OpenStreetMap) para el MVP. | **Rechazada** |
| 5 | 30/09 | Claude | [`prompt-04-matriz-pesos.md`](prompts/prompt-04-matriz-pesos.md): generar la matriz y el script de matplotlib. | Propuso pesos 30 + 25 + 20 + 15 + 15 = 105 % y un gráfico de barras. | Detectamos que los pesos no sumaban 100 %; ajustamos modificabilidad a 10 % y recalculamos el total ponderado a mano antes de aceptar el gráfico. | **Corregida** |
| 6 | 04/10 | Muse Spark 1.3 (harness Opencode) | Revisar `arquitectura.mmd`: ¿cumple E3 (≥2 actores, subgraph, BD, servicio externo, flechas)? | Primer borrador sin `subgraph` y con sintaxis de nube no válida en GitHub. | Se corrigió línea por línea: se agregaron `subgraph Actores/App`, nodo BD y servicio externo, y se validó render con `mermaid-cli` v12. | **Corregida** |
| 7 | 04/10 | Muse Spark 1.3 (harness Opencode) | Redactar ADR-002 y ADR-003 a partir de drivers y matriz. | Borradores con alternativas y consecuencias genéricas, sin citar drivers. | Se reescribieron citando RF-/QA-/R- y con decisión en voz activa; verificación: coherencia matriz → ADR-001 → diagramas. | **Corregida** |
| 8 | 04/10 | Muse Spark 1.3 (harness Opencode) | Generar PNG de `alternativa.puml` y `despliegue.py` sin Graphviz. | Propuso instalar Graphviz con sudo (no disponible) y afirmó que PlantUML renderiza sin `dot`. | Se verificó el error (`forkAndExec` buscando `dot`); se versionó la fuente canonical y se generaron PNG equivalentes con matplotlib, declarándolo en README (Plan B de la guía). | **Corregida** |

## Anexo: prompts

### Prompt 3 — Escenarios de calidad

> Actúa como arquitecto de software. Contexto: RutaSIT Arequipa, 300 buses envían su posición
> cada 10 s y el ETA debe actualizarse en ≤ 15 s. Tarea: redacta 3 escenarios de atributos de
> calidad en formato de seis partes (fuente, estímulo, entorno, artefacto, respuesta, medida).
> El primero debe ser el atributo crítico (rendimiento en tiempo real). Regla: cada medida debe
> ser numérica y verificable; no uses palabras vagas como «rápido», «seguro» o «fácil».

### Prompt 1 — Alternativas de estilo arquitectónico

> Actúa como arquitecto de software senior con experiencia en sistemas de transporte y monitoreo
> en tiempo real para ciudades intermedias.
>
> **Contexto:** sistema «RutaSIT Arequipa» para el Sistema Integrado de Transporte de Arequipa.
> 300 buses con rastreador GPS transmiten su posición cada 10 s; el pasajero ve los buses en un
> mapa y consulta el ETA a su paradero; el operador recibe alertas de desvío/congestión y
> administra rutas y paraderos; ~5 000 pasajeros concurrentes en hora punta.
>
> **Restricciones:** MVP en producción en 1 mes; equipo de 3 developers con Python/Django y
> JavaScript, sin experiencia en DevOps/Kubernetes; hosting bajo (un VPS); los buses transmiten
> por 3G/4G; Ley N.º 29733 de protección de datos.
>
> **Tarea:** propón 3 alternativas de estilo arquitectónico. Para cada una indica fortalezas,
> debilidades, riesgos y qué atributos de calidad favorece o penaliza.
>
> **Formato:** tabla comparativa en Markdown y, al final, tu recomendación justificada.
> No inventes APIs ni capacidades de servicios; si no estás seguro, indícalo.

### Prompt 2 — Crítica adversarial

> Ahora actúa como «abogado del diablo». Critica duramente la alternativa que recomendaste para
> RutaSIT Arequipa: ¿qué supuestos no se cumplen con nuestras restricciones (1 mes, 3 developers,
> un VPS)?, ¿qué podría fallar en producción con 300 buses enviando posición cada 10 s?, ¿qué
> costo oculto tiene? Enumera los 5 riesgos más graves y, para cada uno, una táctica
> arquitectónica de mitigación. No propongas tecnologías inexistentes ni capacidades no
> documentadas.

### Prompt 4 — Matriz de decisión y pesos

> Actúa como arquitecto de software. Con estos drivers (atributo crítico: rendimiento en tiempo
> real, QA-01; plazo de 1 mes, R-01; presupuesto de un VPS, R-03; equipo de 3 developers, R-02),
> propón 5 criterios con pesos que sumen exactamente 100 %, justifica cada peso citando su driver
> y genera un script de matplotlib que dibuje el total ponderado de las 3 alternativas.
