# E8 — Revisión y entrega del grupo

Fecha límite de la guía: **31/10/2026, 23:59**. Repositorio:
https://github.com/F4brici0L4yme/cs-2026b-lab04-grupo-b

## Estado verificable

- [x] E1: árbol editable y escenarios de cuatro atributos.
- [x] E2/E4: tres iteraciones con siete pasos ADD, alternativas y evidencia.
- [x] E5 local: contratos, pruebas, fallos intencionales y reversión documentados.
- [x] E6 técnico: ADR-006/007/008 y C4 validado/exportado.
- [x] E7 técnico: evaluación propia, matriz y bitácora de elaboración asistida.
- [ ] Ratificación humana de prioridades, corrección QA-05 y decisiones ADR.
- [ ] E3: issue al grupo asignado, issue recibido y respuesta con evidencia.
- [ ] E5/E8 remoto: publicar workflow y verificar última ejecución verde.
- [ ] E8: PR de cada integrante, revisión cruzada y merges.
- [ ] E8: etiqueta `v0.8-arquitectura` sobre commit final aprobado.
- [ ] Enlace entregado en Aula Virtual.

Los archivos del informe reflejan esos pendientes; actualizar su estado y
regenerarlos después de la colaboración. El reto opcional (+2) no forma parte
de los entregables obligatorios implementados.

## Distribución propuesta de revisión/PR

| Integrante | Paquete de trabajo sugerido | Revisión sugerida |
|---|---|---|
| Brayan Auccacusi | E1, E2, ADR-006 | Layme |
| Rodrigo Fabricio Layme | E4, E6, diagramas | Castillo |
| Rodrigo Zarun Castillo | E5, E7 y consolidación E8 | Auccacusi |

Es una propuesta, no un registro de aportes realizados. Cada persona revisa el
contenido y publica desde su propia cuenta. Coordinar dependencias de código y
workflow para que cada PR ejecute un conjunto consistente.

## Mensajes de commit sugeridos

1. `E1: arbol de utilidad`
2. `E2: iteracion 1 ADD`
3. `E3: evaluacion ATAM-lite cruzada` (cuando existan hallazgos externos)
4. `E4: iteraciones 2 y 3 ADD`
5. `E5: fitness functions y evidencia de violaciones`
6. `E6: ADR-006 a ADR-008 y C4 actualizado`
7. `E7: riesgos y bitacora IA`
8. `E8: informe README y entrega`

Revisar archivos de cada commit con `git diff`/`git diff --cached`; no crear
ocho commits vacíos ni atribuir autoría de otro integrante.

## Comprobación y cierre remoto

```bash
# Una vez publicados los PR y el workflow:
gh run list --workflow fitness.yml
gh run view ID_DEL_RUN --log-failed
# Tras integrar las revisiones, desde la rama final actualizada:
git tag v0.8-arquitectura
git push origin v0.8-arquitectura
```

Adjuntar al informe los enlaces del run, issues y PR reales antes de marcar
la entrega completa. La configuración actual incluye el badge, pero su estado
depende de GitHub, no del archivo Markdown.
