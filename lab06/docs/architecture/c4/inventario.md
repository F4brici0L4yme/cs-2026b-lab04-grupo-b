# Inventario de elementos C4 — RutaSIT Arequipa (Lab 06)

Elementos del modelo C4, su abstracción y el artefacto de los Laboratorios 04 y 05 del
que proviene cada uno. Este inventario alimenta `workspace.dsl`, la fuente única de las
cinco vistas.

## Personas

| Elemento | Tipo C4 | Qué hace | Origen |
|---|---|---|---|
| Pasajero | Persona | Consulta la ubicación de los buses y su ETA para planificar su viaje. | `docs/architecture/drivers.md` (actores; RF-02, RF-03) y `lab05/historia.md` (HU-06) |
| Operador | Persona | Supervisa la flota, recibe alertas de desvío y administra rutas y paraderos. | `docs/architecture/drivers.md` (actores; RF-04 a RF-07) |

## Sistemas

| Elemento | Tipo C4 | Qué hace | Origen |
|---|---|---|---|
| RutaSIT Arequipa | Sistema de software (propio) | Seguimiento en tiempo real de los buses del SIT: ubicación, ETA y alertas de desvío. | Caso N.º 6; `docs/architecture/drivers.md` |
| Rastreador GPS de los buses | Sistema externo («Externo») | Transmite la posición de cada unidad por red móvil 3G/4G cada 10 s. | `docs/architecture/drivers.md` (RF-01, R-05) y `docs/architecture/diagramas/arquitectura.mmd` |
| Mapas abiertos (OSM) | Sistema externo («Externo») | Provee los tiles y la geometría de referencia del mapa. | `docs/architecture/diagramas/arquitectura.mmd` y `docs/architecture/diagramas/despliegue.py` |

## Contenedores (nivel 2)

| Elemento | Tipo C4 | Tecnología | Origen |
|---|---|---|---|
| API RutaSIT | Contenedor (aplicación) | Python 3.11 / Django | ADR-001 y ADR-003; `diagramas/despliegue.py` |
| Worker ETA/Alertas | Contenedor (aplicación) | Celery | ADR-001 y ADR-003; `diagramas/despliegue.py` |
| Cola y caché | Contenedor (almacén) | Redis | ADR-001 y ADR-003; `diagramas/despliegue.py` |
| Base de datos | Contenedor (almacén) | PostgreSQL | ADR-002; `diagramas/despliegue.py` |

## Componentes del contenedor principal «API RutaSIT» (nivel 3)

| Elemento | Tipo C4 | Qué hace | Origen |
|---|---|---|---|
| Presentación | Componente | Fachada de la API y controlador de monitoreo; recibe las solicitudes REST. | `lab05/diagrama_paquetes.puml` (paquete `presentacion`) |
| Aplicación | Componente | Caso de uso de seguimiento y puertos (repositorio, GPS, notificador, ETA, reloj). | `lab05/diagrama_paquetes.puml` (paquete `aplicacion`) |
| Dominio | Componente | Entidades y reglas de bus, ruta, paradero, ubicación, ETA y alerta de desvío. | `lab05/diagrama_paquetes.puml` (paquete `dominio`) |
| Infraestructura | Componente | Adaptadores que implementan los puertos y persisten/reconstruyen entidades. | `lab05/diagrama_paquetes.puml` (paquete `infraestructura`) |
| Compartido | Componente | Identificadores y tipos comunes del modelo. | `lab05/diagrama_paquetes.puml` (paquete `compartido`) |

## Vistas complementarias

| Vista | Escenario | Origen |
|---|---|---|
| Dinámica | Consulta de seguimiento del pasajero con detección de desvío y alerta (HU-06). | `lab05/diagrama_secuencia.puml` y `lab05/diagrama_actividades.puml` |
| Despliegue «Producción» | VPS único (R-03), buses con rastreador (R-05) y dispositivos de usuario. | `docs/architecture/drivers.md` (R-03, R-05) y `diagramas/despliegue.py` |

## Nivel 4 (código)

El nivel 4 no se redibuja: se enlaza el diagrama de clases del Laboratorio 05, que ya
implementa los componentes del dominio y los puertos del contenedor API:
[`../../../../lab05/diagrama_clases.puml`](../../../../lab05/diagrama_clases.puml)

## Notas de alcance

- Los módulos funcionales del ADR-001 (Ingesta, Flota, ETA, Alertas, Rutas) se realizan
  dentro del monolito; el nivel 3 se modela con los paquetes del Laboratorio 05
  (`diagrama_paquetes.puml`) para cumplir el criterio de coherencia del E3.
- Nginx (proxy) y Grafana (monitoreo) figuran en `diagramas/despliegue.py` del Lab 04,
  pero el equipo acordó dejarlos fuera de las vistas C4 del MVP; la decisión queda
  registrada en `bitacora-ia.md`.
