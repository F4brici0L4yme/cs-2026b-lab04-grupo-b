# Sesión de IA — HU-12

> Registro de esta ejecución. Los resultados reflejan comandos observados en esta sesión.

| Interacción | Solicitud / contexto | Resultado observado | Decisión del equipo |
|---|---|---|---|
| 1 | Revisar guía Lab 12, caso RutaSIT y el código de Labs 05–10. | HU-12 se delimita a distancia ETA sobre trazado; Lab 10 ya tiene ETA no negativa/GPS ausente. | Aceptada; evita duplicar la demostración de Lab 10. |
| 2 | Proponer pruebas antes del cálculo. | La primera corrida falló al importar el módulo aún no implementado. | Aceptada como estado rojo inicial. |
| 3 | Implementar proyección de ubicación y paradero sobre la polilínea. | La primera aserción esperaba un rango menor que la geometría real (2.07 km); la prueba falló. | Corregida la expectativa según tramos conocidos, sin modificar producción. |
| 4 | Conectar el estimador al puerto ETA y probar `consultar_seguimiento`. | La posición “pasada” se consideró desviada porque el trazado terminaba en el paradero. | Corregido el fixture para extender el trazado más allá del paradero. |
| 5 | Ejecutar cobertura y compuertas. | 7 pruebas, 92.96 % cobertura; Ruff, Bandit, Radon y regresiones por separado pasan. | Aceptada; se separaron paths de tests de Labs 05/07/10 tras un fallo de importación. |

Las pruebas nuevas ejercitan el servicio público; no se modificaron las pruebas históricas.
