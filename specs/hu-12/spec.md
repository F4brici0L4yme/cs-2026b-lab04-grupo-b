# HU-12 — Estimar ETA según el trazado restante

## Historia
Como pasajero de RutaSIT, quiero una ETA que considere el trayecto real que queda hasta mi paradero, para recibir una estimación más útil en rutas curvas.

## Criterios de aceptación (Gherkin)

### Escenario 1: ETA por distancia restante
Dado un bus con telemetría vigente y un paradero posterior sobre su ruta
Cuando consulto el seguimiento del bus
Entonces la ETA usa la distancia recorrida sobre el trazado hasta ese paradero y la velocidad configurada

### Escenario 2: GPS ya pasó el paradero
Dado un bus cuya última posición ya superó el paradero consultado en el orden de la ruta
Cuando consulto su seguimiento
Entonces el sistema no devuelve una ETA negativa y representa llegada inmediata según el contrato existente

### Escenario 3: GPS ausente o vencido
Dado un bus sin ubicación GPS utilizable
Cuando consulto su seguimiento
Entonces no se publica una ETA actual y se conserva el estado de datos ausentes/vencidos existente

### Escenario 4: ruta curva
Dado un trazado con segmentos que no son rectos entre la posición y el paradero
Cuando se calcula la distancia restante
Entonces se suman los tramos del trazado desde la proyección de la posición hasta el paradero, sin usar la distancia euclídea directa

### Escenario 5: datos de ruta insuficientes
Dado un trazado que no permite ubicar la posición o el paradero de forma válida
Cuando se solicita la ETA
Entonces el cálculo falla de forma explícita o devuelve el resultado no disponible definido por el servicio, sin inventar una ETA

## Fuera de alcance
Integración con GPS real, mapas externos, aprendizaje de velocidad, cambios de API pública y redefinición de la política de datos ausentes.
