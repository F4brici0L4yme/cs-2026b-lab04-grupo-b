# Plan técnico — HU-12

- Mantener el proyecto por laboratorios y probar la interfaz pública `SeguimientoService.consultar_seguimiento`.
- Reutilizar `Ruta.puntos_trazado`, `Paradero.ubicacion`, telemetría vigente y `EstimadorETASimple` del Lab 05; añadir una política de estimación por distancia restante en un paquete aislado `lab12/src/rutasit_lab12`.
- No modificar las regresiones de Labs 05, 07 ni 10, no agregar dependencias y no tocar el agente de Lab 10.
- Determinar por las pruebas el tratamiento del paradero ya pasado y la proyección sobre el trazado; mantener inalterado el estado SIN_DATOS/SIN_SEÑAL.
