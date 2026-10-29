# E5 — Fitness functions y detección de degradación

| ID | Tipo | Escenario / origen | Regresión detectada | Evidencia |
|---|---|---|---|---|
| FF-01 | Estructural | ADR-001 + capas Lab 05 | Dominio importa aplicación/infraestructura o se invierte una capa | `lint-imports`, contrato layers |
| FF-02 | Estructural | ADR-005 refinado y puertos Lab 05 | Caso de uso/presentación importa adaptador concreto, incluso transitivamente | `lint-imports`, contrato forbidden |
| FF-03 | Calidad | QA-01 | Tiempo de ingesta provoca p95 >15 s o eventos de un minuto no consultables al cierre+15 s | Tres semillas × fases/ráfagas, 36 000 eventos por ensayo; verifica los cinco cierres |
| FF-04 | Calidad | QA-04 | Consulta de respaldo lenta rompe p95 2 s en pico/caché fría | Tres semillas × 0/20/80% aciertos |
| FF-05 | Calidad | QA-02 | Eliminar fallback produce vistas vacías; quitar breaker aumenta llamadas | Caída de 20 min; recuperación y llamadas verificadas |
| FF-06 | Calidad | QA-07 | TTL renueva artificialmente edad GPS | Fuente cruza 30 s mientras entrada sigue en TTL |
| FF-07 | Calidad | QA-05 | Exponer campos ajenos al DTO público | Lista permitida exacta en 100 consultas |

Las pruebas adicionales comprueban transición del breaker, reapertura,
señal ausente/vencida, LRU, claves bus/paradero y eventos fuera de orden.
Resultado local: **24 passed**. Regresión Lab 05: 10 OK; Lab 07: 30 passed,
1 xfailed preexistente por comportamiento de la versión anterior.

## Prueba negativa estructural

`scripts/probar_violaciones.py` crea una copia temporal del paquete en un
repositorio Git aislado y la rama `test/lab08-violaciones`. Ejecuta:

1. Base: 2 contratos cumplidos.
2. Agrega `from rutasit8.aplicacion import seguimiento` a dominio: FF-01 falla,
   exit code 1. Revierte con `git restore`: vuelven los dos contratos.
3. Agrega `from rutasit8.infraestructura import memoria` al caso de uso:
   FF-01 y FF-02 fallan, exit code 1. Revierte: 2 cumplidos, 0 rotos.

La rama y sus cambios son reales dentro del repositorio temporal. No se publica
una violación en la rama del usuario. Salida íntegra en
[violaciones.txt](../../evidencias/violaciones.txt).

## Controles negativos de calidad

La base de ingesta sin optimización supera 15 s; consultas base y solo caché
fría superan 2 s; la vista acoplada deja 1200 respuestas vacías. Las pruebas
exigen que esos controles fallen el escenario: evitan un simulador que siempre
declare éxito. La caché es margen; retirarla con índice eficaz no debe hacer
fallar por sí solo QA-04. Los tests no demuestran tiempos de SQL real.

## Integración continua

`.github/workflows/fitness.yml` ejecuta contratos, pruebas, regresiones,
violaciones reversibles, simulaciones y validación/exportación C4 en cada PR;
también al actualizar `main`/`master` y mediante ejecución manual. Publica las
evidencias como artifact incluso si falla un paso.

**Estado remoto pendiente** hasta publicar cambios y comprobar el run de GitHub.
Un log local exitoso no equivale a un Action verde. Para impedir merges fallidos,
el administrador debe configurar `arquitectura` como comprobación requerida en
la protección de la rama; un workflow por sí solo no bloquea el botón de merge.
