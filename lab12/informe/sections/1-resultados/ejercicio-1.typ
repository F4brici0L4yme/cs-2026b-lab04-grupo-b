= Ejercicios propuestos — HU-12 de RutaSIT

La historia HU-12 estima el tiempo de llegada usando la distancia que queda sobre el trazado real de la ruta. Se integró con el servicio público `SeguimientoService.consultar_seguimiento` y el puerto `IEstimadorETA` existente. Esta sección sigue los entregables E1–E8 de la guía. Las capturas documentan el estado del repositorio y las acciones observadas; cuando un entregable está incompleto se indica en la matriz final.

#set par(justify: true)
#set figure(gap: 0.7em)

#pagebreak()
== E1. Contexto del proyecto y compuertas

Se adaptó `AGENTS.md` al caso RutaSIT y se configuraron compuertas para pruebas con cobertura de ramas mínima de 85 %, Ruff, Bandit, Radon, allowlist de dependencias y regresiones de los Labs 05, 07 y 10. El workflow de GitHub Actions ejecuta `calidad/verificar.py hu-12` en Python 3.12. La allowlist de dependencias funciona como compuerta nueva y evita imports de terceros no aprobados.

#figure(
  image("../../images/e1-quality-gates.png", width: 88%),
  caption: [Ejecución local del verificador y las compuertas de calidad para HU-12.]
)

La captura evidencia la corrida del verificador. En el PR, los workflows `calidad` y `arquitectura` terminaron correctamente; la evidencia de GitHub se incluye en E8.

#pagebreak()
== E2. Especificación, plan y tareas

La especificación contiene cinco escenarios Gherkin: distancia restante, GPS que ya pasó el paradero, GPS ausente o vencido, ruta curva y trazado insuficiente. Incluye la sección «Fuera de alcance». El plan conserva los límites entre laboratorios, reutiliza el contrato del servicio y evita cambios al agente del Lab 10. La lista de tareas define cinco actividades pequeñas para pruebas, cálculo, integración, bordes y regresiones.

#figure(
  image("../../images/e2-spec.png", width: 88%),
  caption: [Archivos de especificación, plan y tareas de HU-12 en el repositorio.]
)

#pagebreak()
== E3. TDD con asistencia de IA

Se registró el estado rojo inicial y la secuencia de correcciones en `sesion-ia.md` y `bitacora-ia.md`. Las pruebas ejercitan el servicio público y cubren ruta curva, posición posterior al paradero, datos ausentes o vencidos, velocidad inválida, ruta no registrada y geometría insuficiente. La última corrida documentada en el informe anterior fue de 8 pruebas HU-12 aprobadas y 95.77 % de cobertura; las regresiones documentadas fueron Lab 05: 10 aprobadas, Lab 07: 30 aprobadas y 1 xfailed, y Lab 10: 5 aprobadas.

#figure(
  image("../../images/e3-tdd.png", width: 88%),
  caption: [Historial de cambios de HU-12 y evidencia del flujo de implementación.]
)

El historial muestra commits por hitos E1, E2 y E3, pero no un commit separado por cada tarea posterior como pide literalmente la guía. Por ello, el TDD está respaldado por las pruebas y la sesión registrada, mientras que el requisito de granularidad de commits queda parcial.

#pagebreak()
== E4. Revisión del Pull Request

El PR #6 recibió análisis asistido y revisión humana. Castillo solicitó cambios por documentación, E5, dependencias del ZIP y un caso de borde. Brayan revisó los cambios posteriores y dejó un comentario explícito de aprobación después de confirmar las correcciones y los checks verdes. El PR fue fusionado. GitHub muestra la aprobación como comentario del PR, no como un evento formal de revisión con estado `APPROVED`.

#figure(
  image("../../images/pr-human-review.png", width: 83%),
  caption: [Salida de `gh pr view 6 --comments`: solicitud de cambios de Castillo y aprobación posterior de Brayan.]
)

#pagebreak()
== E5. Compuertas frente a borrador sin revisar

Se aplicaron a ambas versiones Ruff, Bandit y Radon. Ambas pasan Ruff y Bandit; Radon reporta complejidad A para el borrador y para el estimador final. El borrador usa solo `math`, mientras que la versión final depende del paquete local aprobado `rutasit`. La prueba funcional de ruta curva falla en el borrador (ETA de 3 min) y pasa en la versión final (4 min); el caso de paradero fuera del trazado agrega una compuerta funcional nueva. La cobertura se mide sobre el módulo HU-12 final; no aplica al borrador aislado.

#figure(
  image("../../images/e5-comparison.png", width: 88%),
  caption: [Comparación de la prueba funcional para el borrador y la versión final.]
)

#figure(
  image("../../images/e5-gates-table.png", width: 88%),
  caption: [Registro comparativo de estilo, seguridad, complejidad, dependencias y cobertura para E5.]
)

#pagebreak()
== E6. Mini experimento de productividad

La guía pide que cada integrante implemente dos tareas comparables, una con IA y otra sin IA, en diseño cruzado, y registre tiempos, iteraciones, compuertas al primer intento, defectos y comprensión. El archivo `experimento.csv` está vacío. La tabla siguiente procede de `experimento-demo.csv` y sus valores son ficticios: sirve solo para mostrar el formato y no es resultado ni evidencia del grupo.

#set text(size: 8.5pt)
#table(
  columns: (1.15fr, 1.55fr, 0.65fr, 0.55fr, 0.6fr, 0.75fr, 0.65fr, 0.8fr),
  inset: 4pt,
  align: (left, left, center, center, center, center, center, center),
  fill: (x, y) => if y == 0 { rgb("E5E7EB") } else if calc.even(y) { white } else { rgb("F8FAFC") },
  table.header([Integrante], [Tarea], [Modo], [Min], [Iter. IA], [Compuertas], [Defectos], [Comprende]),
  [Rodrigo], [T-A: paradero fuera de ruta], [Con IA], [28], [3], [5/7], [2], [Sí],
  [Rodrigo], [T-B: bus pasó el paradero], [Sin IA], [35], [N/A], [4/7], [1], [Sí],
  [Brayan], [T-A: paradero fuera de ruta], [Sin IA], [32], [N/A], [4/7], [2], [Sí],
  [Brayan], [T-B: bus pasó el paradero], [Con IA], [24], [2], [6/7], [1], [Sí],
  [Castillo], [T-A: paradero fuera de ruta], [Con IA], [30], [3], [5/7], [1], [Sí],
  [Castillo], [T-B: bus pasó el paradero], [Sin IA], [38], [N/A], [4/7], [2], [No],
)
#set text(size: 10pt)

El promedio ilustrativo es 27.3 minutos con IA frente a 35 minutos sin IA. No se interpreta como mejora observada: los valores no se midieron. El experimento queda pendiente; por ello, aún no se comparan resultados del grupo con los estudios de DORA 2025 y METR 2025, que servirán como referencia para el análisis real #cite(<dora2025>) #cite(<metr2025>).

#pagebreak()
== E7. Bitácora de IA

La bitácora registra siete interacciones, incluyendo fallos detectados por pruebas o compuertas: importación inicial del módulo inexistente, expectativa geométrica incorrecta, fixture insuficiente para el caso de bus pasado, cobertura bajo el umbral, colisión de imports entre laboratorios e incompatibilidad de Bandit con una versión local de Python. Se documentan las decisiones y las correcciones realizadas.

#figure(
  image("../../images/e7-log.png", width: 88%),
  caption: [Extracto de la bitácora de interacciones y detección de errores.]
)

#pagebreak()
== E8. ADR, README y entrega

El repositorio contiene ADR-012 con límites de delegación, compuertas obligatorias, responsabilidad humana, manejo de secretos y licencias. El README añade la sección «Desarrollo asistido por IA (Lab 12)». El PR #6 se fusionó en `master` con el commit `c700065`; la captura muestra el estado de merge. La captura de Actions presenta ejecuciones exitosas de `Calidad Lab 12` y `fitness-functions` para el PR y su merge.

#figure(
  image("../../images/github-pr-merged.png", width: 94%),
  caption: [PR #6 fusionado en `master` con el commit `c700065`.]
)

#figure(
  image("../../images/github-actions-history.png", width: 94%),
  caption: [Historial de GitHub Actions: checks verdes para el PR #6 y el merge.]
)

La política ADR-012 aparece como propuesta pendiente de ratificación. Además, no se encontró la etiqueta de entrega `v1.2-ia`; esos dos puntos impiden marcar E8 como completo.

#pagebreak()
== Revisión final de la rúbrica

#set text(size: 9pt)
#table(
  columns: (0.55fr, 2.55fr, 0.95fr, 2.65fr),
  inset: 5pt,
  align: (left, left, center, left),
  fill: (x, y) => if y == 0 { rgb("E5E7EB") } else if calc.even(y) { white } else { rgb("F8FAFC") },
  table.header([Criterio], [Evidencia revisada], [Estado], [Pendiente / observación]),
  [E1], [AGENTS.md, workflow, verificador y compuertas ejecutadas.], [Cumple], [La allowlist aporta una compuerta adicional.],
  [E2], [Spec con cinco escenarios, plan y cinco tareas.], [Cumple], [Incluye borde de seguridad/datos no disponibles y fuera de alcance.],
  [E3], [Pruebas previas, sesión de IA y pruebas de servicio.], [Parcial], [El historial no tiene un commit individual por cada tarea.],
  [E4], [Análisis asistido, comentario humano de Castillo, aprobación comentada de Brayan, correcciones, merge y CI verde.], [Cumple], [Brayan aprobó en comentario del PR; GitHub no registra un evento formal `APPROVED`.],
  [E5], [Comparación de Ruff, Bandit, Radon, dependencias y criterio funcional; compuerta nueva de trazado.], [Cumple], [La cobertura se aplica al módulo final y no al borrador aislado.],
  [E6], [Plantilla CSV real vacía y tabla demo señalada como ficticia.], [Pendiente], [Realizar el experimento cruzado y comparar honestamente con DORA/METR.],
  [E7], [Bitácora con más de cinco interacciones y errores detectados.], [Cumple], [Incluye detección por pruebas, cobertura y análisis de herramientas.],
  [E8], [ADR-012, sección README, PR fusionado y CI.], [Parcial], [Ratificar el ADR y crear la etiqueta `v1.2-ia`; no se halló tag.],
)
#set text(size: 10pt)

*Conclusión de auditoría:* el informe reúne evidencia por entregable y los resultados de CI/merge, pero la rúbrica completa no se puede declarar satisfecha mientras E6 siga sin mediciones reales. E3 y E8 también conservan observaciones concretas arriba. La tabla demo está identificada como ficticia y no se presenta como dato experimental del grupo.
