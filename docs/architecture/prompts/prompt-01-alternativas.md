# Prompt 01 — Generación de alternativas de estilo arquitectónico

- **Fecha:** 29/09/2026
- **Herramienta:** Claude (asistente de IA)
- **Técnica:** estructura RCRTF (Rol, Contexto, Restricciones, Tarea, Formato)
- **Archivo hermano:** registrado en `bitacora-ia.md`, entrada 2 (decisión: **Rechazada** la recomendación de microservicios)

## Prompt (texto exacto)

```text
Actúa como arquitecto de software senior con experiencia en sistemas de transporte y
monitoreo en tiempo real para ciudades intermedias.

Contexto: sistema "RutaSIT Arequipa" para el Sistema Integrado de Transporte (SIT) de
Arequipa.
- 300 buses con rastreador GPS transmiten su posición cada 10 segundos.
- El pasajero visualiza los buses en un mapa y consulta el tiempo estimado de llegada
  (ETA) a su paradero.
- El operador recibe alertas de desvío de ruta o congestión y administra rutas y paraderos.
- Usuarios concurrentes estimados: ~5 000 pasajeros en hora punta (6:30–8:30 a. m.).

Restricciones:
- Plazo: MVP en producción en 1 mes.
- Equipo: 3 desarrolladores con dominio de Python/Django y JavaScript, sin experiencia
  en DevOps ni Kubernetes.
- Presupuesto: hosting de bajo costo, un único VPS; cualquier servicio de pago debe
  justificarse.
- Tecnología: los buses transmiten por red móvil 3G/4G; se requiere un proveedor de mapas.
- Normativa: Ley N.º 29733 de Protección de Datos Personales.

Tarea: propón 3 alternativas de estilo arquitectónico para el MVP. Para cada una indica
fortalezas, debilidades, riesgos y qué atributos de calidad favorece o penaliza
(rendimiento en tiempo real, disponibilidad, escalabilidad, simplicidad operativa,
modificabilidad).

Formato: tabla comparativa en Markdown y, al final, tu recomendación justificada.

No inventes APIs ni capacidades de servicios; si no estás seguro de algo, indícalo
explícitamente.
```

## Resumen de la respuesta de la IA

Propuesta A — *monolito en capas*: simple y económico, pero con módulos acoplados.
Propuesta B — *microservicios con Kubernetes y Kafka*: escalable, pero con varios
despliegues, varias bases de datos y un broker.
Propuesta C — *monolito modular*: un despliegue con módulos aislados.
La IA **recomendó** la B «por escalabilidad».

## Verificación humana

- Cálculo: `300 buses × (1 posición / 10 s) = 30 eventos/s`. Es una carga que un VPS y una
  cola ligera absorben; no justifica un broker distribuido ni 3 bases de datos.
- La B incumple **R-02** (equipo sin experiencia en DevOps) y **R-03** (presupuesto de un VPS).
- **Decisión del equipo:** descartar la recomendación de la IA y llevar A, B y C a la matriz
  ponderada, donde C resulta ganadora.
