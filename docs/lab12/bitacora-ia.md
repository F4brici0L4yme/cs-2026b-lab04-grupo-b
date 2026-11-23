# Bitácora de IA — Lab 12

1. Lectura del repositorio: el Lab 05 define `SeguimientoService` y el puerto `IEstimadorETA`; decisión: integrar respetando ese puerto.
2. Primer intento de prueba: módulo HU-12 ausente; pytest falla en colección; decisión: registrar rojo y crear módulo en el siguiente ciclo.
3. Cálculo geométrico inicial: prueba de distancia falla porque el umbral esperado no corresponde a la suma de tramos; Ruff y la aserción detectan el error; se corrige el dato de prueba con geometría calculada.
4. Prueba de bus pasado: el servicio marca DESVIADO cuando la ruta acaba en el paradero; fixture corregido para incluir tramo posterior, preservando la regla del dominio.
5. Primera cobertura total: reporta 84.51 % frente a 85 % mínimo y prueba de GPS ausente incorrecta; cobertura y prueba detectan omisión, corregida agregando escenarios de rutas faltantes/velocidad/posición ausente.
6. Prueba conjunta de labs: imports de `rutasit` colisionan entre directorios; pytest detecta el conflicto; se ejecutan regresiones por laboratorio con sus respectivos paths.
7. Bandit local en Python 3.14 informa incompatibilidad AST, aunque CI queda fijado en Python 3.12; se confirma Bandit sin hallazgos en entorno compatible posterior.
