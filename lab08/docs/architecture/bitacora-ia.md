# E7 — Bitácora de elaboración asistida por IA

Inicio: 2026-10-27; revisión de consistencia: 2026-10-28. Asistente: OpenCode
con GPT-6 Sol mediante el entorno de desarrollo.
Encargo del usuario: desarrollar todo el Lab 08 con las guías e informes previos.
Esta tabla resume las solicitudes técnicas desglosadas de ese encargo y las
propuestas/verificaciones realizadas durante la elaboración; **no es una
transcripción literal de mensajes ni de reuniones del grupo**. Las correcciones
son propuestas para revisión humana. No se atribuyen aprobaciones a compañeros,
revisiones a otro grupo ni resultados a servicios que no se ejecutaron.

| # | Solicitud / contexto entregado a IA | Propuesta o hipótesis examinada | Verificación | Resultado para revisión del grupo |
|---|---|---|---|---|
| 1 | Identificar entradas ADD leyendo drivers, ADR-001/002/003, HU-06, C4 y ADR-005 | Mantener arquitectura y ampliar carga de 300 a 1200 buses | Lectura de archivos originales; cálculo 1200/10 =120 eventos/s | Propuesta incorporada a `entradas.md`; tres personas y un VPS, no equipo de cinco del ejemplo docente |
| 2 | Proponer escenarios de seis partes y prioridad H/M/L para cuatro atributos | Candidato inicial QA-05 (H,H) por crecimiento y privacidad | R-04/HU-06 ya excluyen datos personales; DTO cerrado y prueba de 100 respuestas | Corrección propuesta a (M,L) para ese escenario acotado, pendiente confirmación humana; no implica seguridad integral |
| 3 | Comparar ≥3 tácticas para QA-01 respetando plazo y presupuesto | Optimización por evento vs más workers vs segundo VPS vs microservicios | Simulación: base 99,919 s, optimizada 7,616 s en ráfaga; sensibilidad ×3 falla | Seleccionar optimización como hipótesis; rechazar cambio automático de estilo; declarar que 6 ms no es una medición |
| 4 | Evaluar rendimiento de consulta y trade-off de caché | Solo caché podría ser suficiente si hay muchos aciertos | 80% aciertos en pico: 91 843,044 ms; índice+caché fría: 256,663 ms | Rechazar caché como sustituto de respaldo eficiente; probar 0% aciertos y servicio ×1,5 |
| 5 | Revisar frescura de HU-06 al reutilizar Decorator | TTL vigente podría hacer parecer actual una captura antigua | Prueba 29,5→30,5 s; TTL aún vigente pero dato ya supera 30 s | Validación por timestamp de captura en cada respuesta; prueba FF-06 |
| 6 | Comparar disponibilidad durante caída de mapas de 20 min | Reintentos solos vs fallback vs breaker | Ejecución del prototipo: 3600→42 llamadas y 1200→0 vistas vacías | Seleccionar breaker+fallback; exponer límite de concurrencia y timeout simulado |
| 7 | Evaluación adversarial: cuestionar capacidad e interpretar carga | FP-01: 50 000 consultas implican 50 000 simultáneas y obligan a microservicios | La guía expresa volumen, no concurrencia; 50 000/3600=13,89 req/s bajo S-01 | **Falso positivo refutado**; conservar R7 por distribución desconocida. Hipótesis adversarial propia, no issue externo |
| 8 | Evaluación adversarial del modelo C4 | FP-02: cuatro contenedores contradicen monolito modular | C4 original ya tenía API, worker, Redis y BD; ADR-001 permite ese despliegue | **Falso positivo refutado**: contenedor C4 no equivale a microservicio de negocio |
| 9 | Convertir reglas de arquitectura en contratos | Atribuir a ADR-005 una separación de arranque ya existente | `lab07/src/rutasit/servicio.py` construye adaptadores en `__init__` | Corregir trazabilidad: separación explícita es un refinamiento del Lab 08, apoyado por puertos del Lab 05 |
| 10 | Verificar contratos, pruebas y modelo antes del informe | Un conjunto de pruebas verdes podría no detectar regresiones | Rama temporal: 2 kept→1 broken→2 kept y 2 broken→2 kept; controles negativos de rendimiento; Structurizr exit 0 | Evidencia real en `evidencias/`; no afirmar workflow remoto verde hasta publicarlo |
| 11 | Revisar coherencia entre QA-01 y FF-03 | Hipótesis a corregir: «100% dentro de 15 s» y backlog final equivalen a completar cada minuto a cierre+15 s | Se añadió una comprobación de terminación por cada minuto; se regeneraron tabla y JSON | Ya no se confunden las tres medidas y se verifica cada compromiso de QA-01 |

## Evidencia y límites

- [Resultados numéricos](../../evidencias/resultados.md) y JSON con tres semillas.
- [Pruebas](../../evidencias/pytest.txt), [contratos](../../evidencias/import-linter.txt)
  y [violaciones revertidas](../../evidencias/violaciones.txt).
- [Modelo validado](../../evidencias/structurizr.txt).
- [ATAM-lite](atam-lite.md): R1 y otros riesgos abiertos; no se ocultan los casos
  donde la simulación falla al modificar supuestos.
- Pendiente del grupo: ratificar prioridades/ADR, completar intercambio E3,
  revisar PR individuales, publicar y comprobar Actions antes del tag.
