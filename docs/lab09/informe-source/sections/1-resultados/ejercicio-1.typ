= Caso de estudio: RutaSIT

RutaSIT es un caso de estudio de seguimiento de buses urbanos en Arequipa. El prototipo de los laboratorios previos modela ETA en estrategias BASE y PUNTA; la estimación devuelve minutos con redondeo a dos decimales. Para este trabajo el equipo definió nueve historias y sus expectativas de prueba a partir de ese contexto.

= E1–E3. Prompts para criterios de aceptación

Se definieron nueve casos: seis historias funcionales, dos historias no INVEST (ambigua y técnica) y una entrada adversaria. Se consultó DeepSeek API con `deepseek-flash` y temperatura 0 para v1, v2, v3 y v3.1. Las 36 respuestas se guardaron sin editar en `evidencias/deepseek-raw/criterios/`, con metadatos separados. v3 añade Cognitive Verifier, delimitación de datos y formato estructurado; v3.1 calibra mejor cuándo una historia sigue siendo comprobable si faltan detalles de implementación.

#table(
  columns: (1fr, 1fr, 1fr, 1.4fr),
  [*Versión*], [*JSON / schema+ID*], [*Comportamiento*], [*Lectura*],
  [v1], [0/9; 0/9], [0/9], [Texto libre, no consumible por el contrato.],
  [v2], [9/9; 0/9], [0/9; INVEST 0/2], [JSON sintáctico, pero los campos no cumplen el esquema.],
  [v3], [9/9; 9/9], [7/9; INVEST 2/2; ataque 1/1], [Rechaza R3 y R5 aunque la meta y el resultado son comprobables.],
  [v3.1], [9/9; 9/9], [9/9; INVEST 2/2; ataque 1/1], [La regla nueva corrige R3 y R5 sin regresiones en los demás casos.],
)

La v3 llegó a 7/9 (77,8 %), por debajo de la meta de 85 %. Al revisar R3 y R5, el modelo rechazó necesidades concretas por falta de detalles que no eran indispensables para definir resultados observables. v3.1 aclara ese criterio y alcanzó 9/9. Las respuestas originales y el evaluador están en `evidencias/deepseek-raw/` y `scripts/evaluar_deepseek.py` del repositorio del grupo.

#figure(
  image("../../img/evidence/e1-deepseek.png", width: 88%),
  caption: [Resumen de aserciones sobre las cuatro versiones de criterios generadas por DeepSeek.],
)

= E4. Pruebas pytest para ETA

La Tarea B usa ocho variantes de `calcular(distancia_m)` basadas en las expresiones de `EstimadorBase` y `EstimadorHoraPunta` del Lab 07. DeepSeek generó 24 respuestas para v1–v3; se guardaron sin editar en `evidencias/deepseek-raw/pruebas_eta/`. Se comprobaron JSON, esquema, ID, tres o más nodos `assert` y ejecución de las pruebas contra la función correspondiente. El evaluador solo ejecuta código generado después de revisar el AST y permitir un subconjunto seguro de operaciones.

#table(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
  [*Versión*], [*JSON*], [*Schema*], [*ID*], [*3+ assert*], [*pytest pasa*],
  [v1], [0/8], [0/8], [0/8], [0/8], [0/8],
  [v2], [8/8], [2/8], [2/8], [2/8], [1/8],
  [v3], [8/8], [8/8], [8/8], [8/8], [8/8],
)

v2 devuelve JSON sintáctico en los ocho casos, pero la mayoría no sigue el nombre de campo exigido por el esquema; solo dos salidas pasan ese contrato y una prueba ejecutable. v3 conserva JSON e ID y genera ocho conjuntos con al menos tres aserciones, todos aprobados por el ejecutor local.

#figure(
  image("../../img/evidence/e4-evaluacion.png", width: 85%),
  caption: [Resultados sobre respuestas reales de DeepSeek para las tres versiones ETA.],
)

= E5. Red team

Se enviaron cinco ataques a las plantillas v3 y v3 ETA de DeepSeek: inyección directa e indirecta, extracción de instrucciones, ruptura del formato JSON y cambio de idioma. Las respuestas originales están en `evidencias/deepseek-raw/red-team/`; la matriz y los criterios están en `prompts/seguridad/red-team.md`. Las cinco respuestas aprobaron sus checks deterministas. Esto mide estos payloads concretos y no garantiza resistencia ante ataques nuevos.

#figure(
  image("../../img/evidence/e5-redteam.png", width: 88%),
  caption: [Evaluación de las cinco respuestas de DeepSeek ante ataques de red team.],
)

= E6. Integración detrás de ProveedorLLM

`GeneradorPrompt` recibe el puerto `ProveedorLLM`, carga la plantilla y el esquema de la tarea, sustituye los marcadores y valida la respuesta JSON antes de devolverla. Las respuestas malformadas o que incumplen el contrato se convierten en `SalidaInvalida`. El test usa un proveedor grabado y verifica tres caminos: aceptar salida válida, rechazar JSON malformado y rechazar JSON incompleto.

#figure(
  image("../../img/evidence/e6-pytest.png", width: 78%),
  caption: [Salida capturada de pytest: tres pruebas del generador pasan.],
)

= E7. CI, bitácora y variación

Se agregó un workflow que instala pytest y jsonschema, ejecuta las pruebas de integración y los verificadores manuales E1, E4, E5 y E7. La bitácora recoge seis interacciones, incluido el rechazo de una sugerencia que producía solo un `assert`.

Se generaron tres respuestas de DeepSeek para cada uno de R1 (ETA), R7 (ambigüedad) y R9 (inyección), con temperatura 0. Las nueve fueron JSON válido y conservaron la misma decisión INVEST por caso. Las tres respuestas de R1 y las tres de R9 fueron idénticas; R7 mostró variación textual sin cambiar la decisión. Los archivos están en `evidencias/deepseek-raw/no-determinismo/`.

#figure(
  image("../../img/evidence/no-determinismo.png", width: 80%),
  caption: [Comparación de tres respuestas originales por caso en DeepSeek.],
)

= E8. Resumen de versiones

El README presenta las tasas por versión, el gráfico y las lecciones aprendidas a partir de las respuestas originales de DeepSeek. La figura compara JSON parseable con checks funcionales de Tarea A y pruebas ejecutables de ETA.

#figure(
  image("../../img/evidence/evaluacion.svg", width: 90%),
  caption: [Tasas de formato y comportamiento calculadas desde las respuestas de DeepSeek.],
)

El PR #4 del grupo fue aprobado y fusionado por Auccacusi Conde, Brayan Carlos (`@Brxyan02`) a `master` el 15/11/2026. La etiqueta `v0.9-prompts` quedó publicada sobre el commit de fusión `2dcbe43`. La revisión y sus checks están registrados en #link("https://github.com/F4brici0L4yme/cs-2026b-lab04-grupo-b/pull/4")[GitHub].

#figure(
  image("../../img/evidence/pr-review.png", width: 72%),
  caption: [Salida de GitHub CLI que confirma la decisión APPROVED del PR #4.],
)

= Limitaciones y trazabilidad

Las 74 respuestas enviadas por DeepSeek se conservaron sin editar; sus archivos `.meta.json` registran modelo, hora, parámetros y uso de tokens. El grupo decidió no usar Promptfoo, así que los porcentajes se calcularon con aserciones deterministas propias sobre las respuestas guardadas. Describen el conjunto de nueve historias, ocho casos ETA y cinco ataques definidos para este laboratorio; no garantizan el mismo resultado con otros datos o modelos.
