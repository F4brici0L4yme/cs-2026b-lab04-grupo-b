# Matriz de decisión — RutaSIT Arequipa

## Alternativas

- **A. Monolito en capas:** una sola aplicación organizada en capas (presentación, negocio,
  datos). La ingesta GPS y el cálculo de ETA se ejecutan dentro del mismo proceso de la API,
  sin una cola intermedia. Es el camino más directo y conocido por el equipo.
- **B. Microservicios con broker de eventos:** servicios independientes (ingesta, ETA, alertas,
  rutas) comunicados por un broker (Kafka/RabbitMQ) y una base de datos por servicio. Escala de
  forma independiente, pero multiplica despliegues y piezas de infraestructura.
- **C. Monolito modular:** un único despliegue en Django con módulos bien delimitados (Ingesta,
  Flota, ETA, Alertas, Rutas) que se comunican solo por interfaces públicas; la ingesta se
  desacopla con una cola ligera (Redis) y cada módulo tiene su propio esquema en PostgreSQL.

## Criterios y pesos (deben sumar 100 %)

| Criterio                    | Peso | Justificación (driver relacionado)                                                   |
|-----------------------------|------|--------------------------------------------------------------------------------------|
| Rendimiento en tiempo real  | 30 % | QA-01: es el atributo crítico; 300 buses cada 10 s y ETA ≤ 15 s.                     |
| Tiempo de entrega           | 25 % | R-01: el MVP debe estar en producción en 1 mes.                                       |
| Costo operativo             | 20 % | R-03: presupuesto bajo, un único VPS.                                                 |
| Simplicidad operativa       | 15 % | R-02: 3 developers sin experiencia en DevOps.                                         |
| Modificabilidad             | 10 % | QA-03 e interoperabilidad: nuevas rutas y orígenes de datos sin tocar los demás módulos. |

> Los pesos suman 100 % (30 + 25 + 20 + 15 + 10). La IA propuso inicialmente 15 % para
> modificabilidad (total 105 %); se corrigió al 10 % tras la verificación (ver bitácora, entrada 5).

## Matriz (puntaje 1 = muy malo … 5 = excelente)

| Criterio (peso)                 | A. Capas | B. Microservicios | C. Monolito modular |
|---------------------------------|:--------:|:-----------------:|:-------------------:|
| Rendimiento en tiempo real (30 %) | 3      | 5                 | 4                   |
| Tiempo de entrega (25 %)        | 5        | 2                 | 4                   |
| Costo operativo (20 %)          | 5        | 2                 | 5                   |
| Simplicidad operativa (15 %)    | 5        | 1                 | 4                   |
| Modificabilidad (10 %)          | 2        | 5                 | 4                   |
| **Total ponderado**             | **4,10** | **3,05**          | **4,20**            |

Total ponderado = Σ (peso × puntaje). Por ejemplo, para C:
`0,30×4 + 0,25×4 + 0,20×5 + 0,15×4 + 0,10×4 = 1,20 + 1,00 + 1,00 + 0,60 + 0,40 = 4,20`.

El gráfico comparativo se genera con el script versionado
[`diagramas/matriz_decision.py`](diagramas/matriz_decision.py) (matplotlib) y su imagen queda en
`diagramas/img/matriz-decision.png`, de modo que la figura puede regenerarse si cambian los pesos.

## Verificación de una afirmación de la IA

La IA recomendó **microservicios con Kafka** «por escalabilidad». El equipo lo verificó con un
cálculo simple: 300 buses × 1 posición / 10 s = **30 eventos por segundo**, una carga que una
cola ligera (Redis) y un solo proceso de ingesta absorben sin dificultad. Un broker distribuido
con 3 brokers y bases de datos por servicio excede R-02 (equipo sin DevOps) y R-03 (un VPS).
La afinación de la matriz es coherente con ese cálculo. Como segunda verificación, la IA afirmó
que la API de Google Maps entrega el ETA de transporte público «gratis e ilimitada»; se comprobó
en la documentación oficial que requiere una cuenta de facturación, por lo que se descartó ese
supuesto y se optó por tecnologías de mapas abiertas (ver bitácora, entrada 4).

## Conclusión

Elegimos la alternativa **C (monolito modular)** porque obtiene el mayor total ponderado (4,20),
respeta el plazo de 1 mes y el tamaño del equipo, y aun así aísla la ingesta en cola para
sostener el atributo crítico (rendimiento en tiempo real). La diferencia con la alternativa A
(4,10) es pequeña y se explica por la modificabilidad: los módulos del monolito modular pueden
extraerse como servicios en el futuro si la flota supera los 600 buses.

Ver [ADR-001](adr/001-estilo-arquitectonico.md).
