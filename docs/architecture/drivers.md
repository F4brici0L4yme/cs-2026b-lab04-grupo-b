# Drivers arquitectónicos — RutaSIT Arequipa

> **Caso N.º 6.** Seguimiento en tiempo real de los buses del Sistema Integrado de Transporte
> (SIT) de Arequipa. Actores: **pasajero**, **bus (GPS)** y **operador**.
> Atributo de calidad crítico del caso: *rendimiento en tiempo real* — 300 buses envían su
> posición cada 10 s y el tiempo estimado de llegada (ETA) se actualiza en ≤ 15 s.

## 1. Requisitos funcionales clave

| ID    | Requisito                                                                        | Actor      | Prioridad |
|-------|----------------------------------------------------------------------------------|------------|-----------|
| RF-01 | El bus (rastreador GPS) transmite su posición cada 10 segundos.                   | Bus (GPS)  | Alta      |
| RF-02 | El pasajero visualiza la posición de los buses sobre un mapa en tiempo real.      | Pasajero   | Alta      |
| RF-03 | El pasajero consulta el tiempo estimado de llegada (ETA) a su paradero.           | Pasajero   | Alta      |
| RF-04 | El sistema genera alertas de desvío de ruta o de congestión para el operador.     | Operador   | Alta      |
| RF-05 | El operador administra rutas y paraderos (registrar, editar y desactivar).        | Operador   | Media     |
| RF-06 | El operador consulta un panel con el estado de la flota (buses activos / sin señal). | Operador | Media     |

## 2. Atributos de calidad (ordenados por prioridad)

1. **Rendimiento en tiempo real** — es el atributo crítico del caso: con 300 buses enviando
   posición cada 10 s y un ETA que debe refrescarse en ≤ 15 s, cualquier retraso en la ingesta
   o en el cálculo vuelve inútil el servicio para el pasajero que espera en el paradero.
2. **Disponibilidad** — la pérdida de señal de un bus o la caída de un servicio externo (mapas)
   no debe dejar al pasajero sin información: el sistema conserva y muestra la última posición
   conocida y el ETA degradado.
3. **Escalabilidad** — el SIT proyecta incorporar nuevas rutas y hasta duplicar la flota
   (600 buses) sin rediseñar la arquitectura.
4. **Simplicidad operativa y costo** — el equipo es pequeño y el presupuesto bajo; el sistema
   será operado por las mismas 3 personas que lo construyen.
5. **Interoperabilidad** — integración con la geometría de rutas y paraderos del SIT y con un
   proveedor de mapas, sin acoplar el núcleo a un proveedor concreto.

## 3. Restricciones

| ID   | Tipo        | Restricción                                                                                                             |
|------|-------------|-------------------------------------------------------------------------------------------------------------------------|
| R-01 | Plazo       | MVP en producción en 1 mes.                                                                                              |
| R-02 | Equipo      | 3 desarrolladores con dominio de Python/Django y JavaScript; sin experiencia en DevOps ni Kubernetes.                    |
| R-03 | Presupuesto | Hosting de bajo costo: un único VPS. Cualquier servicio de pago debe justificarse.                                       |
| R-04 | Normativa  | Ley N.º 29733 de Protección de Datos Personales: la ubicación se asocia a la unidad (bus), no a datos personales del conductor. |
| R-05 | Tecnología  | Los buses transmiten por red móvil 3G/4G; se requiere integración con un proveedor de mapas.                             |

## 4. Escenarios de atributos de calidad

| ID    | Atributo               | Fuente                | Estímulo                                              | Entorno                          | Artefacto              | Respuesta                                                                                     | Medida                                                        |
|-------|------------------------|-----------------------|-------------------------------------------------------|----------------------------------|------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| QA-01 | Rendimiento en tiempo real | 300 buses emisores | Cada bus envía su posición GPS cada 10 s.             | Operación normal, hora punta (6:30–8:30 a. m.). | Módulo de ingesta y módulo de ETA. | El sistema absorbe las posiciones y actualiza el ETA del paradero consultado.          | p95 del ETA ≤ 15 s; 100 % de las posiciones del minuto procesadas. |
| QA-02 | Disponibilidad         | Proveedor de mapas (servicio externo) | El proveedor de tiles deja de responder.              | Operación normal.                | Módulo de visualización. | Se muestra la última posición conocida y un ETA degradado; al volver el proveedor se restablece el mapa. | 0 pantallas vacías; recuperación ≤ 5 min; el error se informa al usuario. |
| QA-03 | Escalabilidad          | Crecimiento de la flota | La flota pasa de 300 a 600 buses enviando posición cada 10 s. | Operación normal tras 6 meses.   | Motor de ingesta y base de datos. | La arquitectura absorbe el doble de eventos sin rediseño.                                     | CPU del VPS < 70 %; p95 del ETA ≤ 15 s con 600 buses.          |
