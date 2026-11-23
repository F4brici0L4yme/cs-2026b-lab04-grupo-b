= HU-12: ETA según la distancia restante de la ruta

Se añadió `EstimadorETADeRuta`, que implementa el puerto `IEstimadorETA` existente y calcula la distancia acumulada sobre los segmentos de la ruta entre la proyección GPS y el paradero. La consulta pública probada es `SeguimientoService.consultar_seguimiento`.

== Pruebas y compuertas

Las pruebas cubren una ruta curva, un bus que ya pasó el paradero, trazado insuficiente, ausencia de ubicación en el estimador, velocidad inválida, ruta no registrada y GPS vencido. Resultado local: 7 pruebas aprobadas y 92.96 % de cobertura del módulo HU-12. Ruff, Bandit y Radon (sin complejidad C o superior) pasan en el entorno Python 3.13; las regresiones separadas de Lab 05 (10), Lab 07 (30 aprobadas y 1 xfailed) y Lab 10 (5) también pasan.

== Evidencia pendiente

E4 requiere revisión real de otro integrante y revisión automática sobre el PR. En E5, una prueba adicional falla para el borrador lineal: estima 3 minutos frente a 4 por el trazado; queda pendiente ejecutar la matriz completa de compuertas sobre ambos árboles. E6 requiere los tiempos y observaciones del experimento cruzado del grupo. La comparación posterior usará la evidencia de METR #cite(<metr2025>) y DORA #cite(<dora2025>). Estos resultados quedan pendientes y no se sustituyen por datos estimados.
