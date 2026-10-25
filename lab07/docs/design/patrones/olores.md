# Olores detectados (E1) — RutaSIT

Fuente: `src/rutasit/antes/servicio.py` + `radon cc -s -a` (consultar C(18), promedio B(7.0)).

| # | Olor (líneas) | Patrón propuesto | SOLID | Decisión |
|---|---|---|---|---|
| 1 | `if/elif` por algoritmo ETA (43-48) que crece con cada algoritmo | Strategy + Factory | OCP | Aceptado: `EstimadorBase` / `EstimadorHoraPunta` + `FabricaETAs` |
| 2 | Servicio conoce SDK GPS (dict vs tupla, 51-70) | Adapter | LSP, DIP | Aceptado: `GpsAdapterA/B` → `PuertoGPS` |
| 3 | Reintentos duplicados A/B (52-68) | Decorator | SRP, OCP | Aceptado: `ConReintentos` solo ante `TimeoutError` |
| 4 | Condicionales sobre `bus.estado` (33-39) | State | LSP | Aceptado: coincide con máquina Lab 05 |
| 5 | Avisos armados a mano sms/panel (75-84) | Observer | SRP, OCP | Aceptado: `PublicadorEventos` + 2 suscriptores |
| 6 | `if/elif` LLM + validaciones mezcladas (88-101) | Strategy + Chain | SRP | Aceptado: `ProveedorLLM` + 3 guardrails |
| 7 | `FabricaGPS` como Singleton | Singleton | — | Rechazado: estado global, impide inyectar fakes en pruebas |
| 8 | Abstract Factory para familias GPS | Abstract Factory | — | Rechazado: no hay familias, sobreingeniería (patternitis) |
