-- Diseño PostgreSQL de referencia (ADR-002/007). No ejecutado como benchmark.
CREATE SCHEMA IF NOT EXISTS eta;
CREATE TABLE IF NOT EXISTS eta.ultimo_eta (
    bus_id text NOT NULL,
    paradero_id text NOT NULL,
    evento_id bigint NOT NULL,
    capturada_en timestamptz NOT NULL,
    eta_min double precision NOT NULL CHECK (eta_min >= 0),
    PRIMARY KEY (bus_id, paradero_id)
);
-- La PK provee el índice compuesto. No añadir un índice idéntico duplicado.
-- Parámetros de ejemplo para el driver: :bus, :paradero, :evento, :captura, :eta.
-- INSERT INTO eta.ultimo_eta VALUES (:bus, :paradero, :evento, :captura, :eta)
-- ON CONFLICT (bus_id, paradero_id) DO UPDATE SET
--   evento_id = EXCLUDED.evento_id, capturada_en = EXCLUDED.capturada_en,
--   eta_min = EXCLUDED.eta_min
-- WHERE EXCLUDED.evento_id > eta.ultimo_eta.evento_id
--   AND EXCLUDED.capturada_en >= eta.ultimo_eta.capturada_en;
-- SELECT evento_id, capturada_en, eta_min FROM eta.ultimo_eta
-- WHERE bus_id = :bus AND paradero_id = :paradero;
-- Los IDs se asumen monotónicos por unidad; un reinicio de secuencia requiere
-- una época persistida o identificador global. La deduplicación de alertas y el
-- historial de posiciones siguen en su propia transacción (ADR-003).
