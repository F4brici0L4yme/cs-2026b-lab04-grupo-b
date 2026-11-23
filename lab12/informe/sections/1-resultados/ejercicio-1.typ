= HU-12: ETA según la distancia restante de la ruta

Se añadió `EstimadorETADeRuta`, que implementa el puerto `IEstimadorETA` existente y calcula la distancia acumulada sobre los segmentos de la ruta entre la proyección GPS y el paradero. La consulta pública probada es `SeguimientoService.consultar_seguimiento`.

== Pruebas y compuertas

Las pruebas cubren una ruta curva, un bus que ya pasó el paradero, trazado insuficiente, ausencia de ubicación en el estimador, velocidad inválida, ruta no registrada y GPS vencido. Resultado local: 8 pruebas aprobadas y 95.77 % de cobertura del módulo HU-12. Ruff, Bandit y Radon (sin complejidad C o superior) pasan en el entorno Python 3.13; las regresiones separadas de Lab 05 (10), Lab 07 (30 aprobadas y 1 xfailed) y Lab 10 (5) también pasan.

== Evidencia pendiente

En E4, Castillo revisó el PR y solicitó cambios; la revisión asistida identificó los mismos puntos. Se aplicaron las correcciones y queda pendiente la revisión de seguimiento de Castillo. En E5, la misma prueba funcional falla para el borrador lineal (3 min) y pasa para el estimador por ruta (4 min); Ruff, Bandit, Radon y dependencias aprobadas pasan en ambos. La cobertura se exige al módulo final. E6 requiere los tiempos y observaciones del experimento cruzado del grupo. La comparación posterior usará la evidencia de METR #cite(<metr2025>) y DORA #cite(<dora2025>). Estos resultados quedan pendientes y no se sustituyen por datos estimados.


== Revisión cruzada del PR

Castillo revisó el PR y solicitó cambios. Coincidimos en los hallazgos y corregimos el estado de la documentación, la evidencia comparativa, el paquete fuente y las pruebas de borde.

#figure(image("../../images/revision-pr-castillo.png", width: 96%), caption: [Captura del comentario de revisión de Castillo en el PR #6.])


#figure(image("../../images/ci-pr-6.png", width: 96%), caption: [Estado final de los workflows `calidad` y `arquitectura` del PR #6.])
