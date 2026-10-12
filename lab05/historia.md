# HU-06: Seguimiento de buses y ETA

**Identificador:** HU-06  
**Rol principal:** Pasajero del SIT  
**Caso:** RutaSIT Arequipa (caso asignado 6)

## Historia

Como [Pasajero del SIT], quiero [ver la ubicación en tiempo real de los buses y su ETA] para [planificar mi viaje y saber si la unidad sufrió un desvío].

## Criterios de aceptación (BDD)

### Escenario 1: actualización de ubicación y ETA en un paradero

**Dado** que el bus está en servicio, tiene una ruta asignada y la última coordenada GPS es válida y reciente (no mayor a 30 segundos)  
**Cuando** el pasajero consulta el bus y un paradero de esa ruta  
**Entonces** el mapa presenta la última ubicación recibida y el sistema devuelve el ETA calculado para ese paradero; el objetivo de servicio es actualizarlo en un máximo de 15 segundos.

### Escenario 2: desvío de ruta y alerta

**Dado** que el bus está en servicio y su ubicación GPS reciente está fuera del trazado de la ruta por encima de la tolerancia configurada  
**Cuando** RutaSIT procesa esa posición  
**Entonces** el estado del bus pasa a `DESVIADO`, se crea una alerta asociada al bus y a la ubicación detectada, y el sistema encola una notificación para el operador.

## Reglas de interpretación

- La ubicación se refiere a la unidad de transporte; este modelo no almacena nombre, DNI, teléfono ni otros datos personales del conductor.
- Una coordenada obsoleta no cambia el estado del bus ni genera una alerta de desvío.
- Los 15 segundos son un objetivo verificable de extremo a extremo, no una garantía demostrada por este esqueleto.
