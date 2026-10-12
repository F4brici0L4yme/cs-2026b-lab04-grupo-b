# Laboratorio 05: Diseño UML de RutaSIT

Entregables de diseño para el caso 6, RutaSIT Arequipa. Las fuentes UML son los archivos `.puml` y `diagrama_estados.mmd`; los SVG de `img/` son sus vistas renderizadas.

## Entregables

- [HU-06](historia.md)
- [E1: clases](diagrama_clases.puml)
- [E2: secuencia](diagrama_secuencia.puml)
- [E3: estados](diagrama_estados.mmd)
- [E4: actividades](diagrama_actividades.puml)
- [E5: paquetes](diagrama_paquetes.puml)
- [E6: código y round-trip](src/rutasit/README.md) · [registro](round-trip.md)
- [E7: consistencia](consistencia.md) · [bitácora IA](bitacora-ia.md)

## Ejecutar el esqueleto

Requiere Python 3.11 o posterior; el dominio solo usa la biblioteca estándar.

```bash
cd lab05
PYTHONPATH=src python -m unittest discover -s tests -v
```

La geocerca y el ETA son implementaciones didácticas; antes de usarlas en producción se deben validar con geometría oficial, datos de tráfico y pruebas de carga.
