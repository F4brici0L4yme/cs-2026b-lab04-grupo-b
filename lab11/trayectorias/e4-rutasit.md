# Trayectoria E4 — agente RutaSIT

Consulta: ETA de SIT-101 y reporte del desvío confirmado de SIT-201.

1. **Consultar ETA solicitado.** `tiempo_llegada` — aprobación humana: **no requerida**. Resultado: `{'bus_id': 'SIT-101', 'paradero_id': 'P-03', 'eta_min': 4.5, 'estado': 'ACTUAL'}`
2. **Verificar que SIT-201 sigue desviado.** `buses_en_ruta` — aprobación humana: **no requerida**. Resultado: `{'result': [{'bus_id': 'SIT-201', 'ruta_id': 'R-02', 'estado': 'DESVIADO', 'siguiente_paradero': 'P-08'}]}`
3. **Registrar evidencia confirmada.** `reportar_desvio` — aprobación humana: **sí**. Resultado: `{'result': 'Creado reportes/DESVIO-05.md'}`

La aprobación de `reportar_desvio` corresponde a la instrucción explícita del usuario de completar el laboratorio.
