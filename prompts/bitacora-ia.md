# Bitácora de interacciones con ChatGPT — Lab 09

| # | Interacción | Hallazgo/decisión |
|---|---|---|
| 1 | Pedí criterios de aceptación desde una historia ETA | Se fijó contrato JSON y comprobación de escenarios. |
| 2 | Pedí valorar la historia vaga R7 | Se rechazaron escenarios inventados y se formularon preguntas al PO. |
| 3 | Pedí probar el caso R9 con texto de inyección | Se conservó la necesidad original de filtrar por ruta. |
| 4 | Pedí que v2 generara pruebas ETA | La respuesta incluyó un solo `assert`; no cumplía la aserción mínima. |
| 5 | Pedí ampliar las pruebas ETA a éxito y borde | Se pasó a v3 con al menos tres aserciones ejecutables. |
| 6 | Pedí revisar el manejo del comentario adversario E8 | Se detectó que el comentario había alterado el snippet y se corrigió el caso para que el comentario no cambiara el código probado. |

## Variación observada

Se generaron tres respuestas v3 para los mismos casos R1, R7 y R9. Las tres conservaron el formato JSON y la misma decisión INVEST por historia, con variación en redacción y escenarios. Los archivos individuales y la comparación están en `evidencias/no-determinismo/`.
