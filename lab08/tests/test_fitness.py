"""Escenarios convertidos en compuertas ejecutables (E5)."""

import pytest

from fitness.disponibilidad import MapasSimulados, Reloj, simular
from fitness.rendimiento import simular_consultas, simular_ingesta
from rutasit8.aplicacion.seguimiento import ConsultaSeguimiento
from rutasit8.arranque import construir
from rutasit8.dominio import LecturaETA
from rutasit8.infraestructura.cache import ConCacheETA
from rutasit8.infraestructura.memoria import RepositorioMemoria
from rutasit8.infraestructura.resiliencia import CircuitoAbierto, ConCircuitBreaker
from rutasit8.presentacion import consultar


@pytest.mark.parametrize("semilla", [7, 19, 42])
@pytest.mark.parametrize("rafagas", [False, True])
def test_ff03_1200_buses_eta_menos_15s(semilla, rafagas):
    r = simular_ingesta(semilla=semilla, rafagas=rafagas)
    assert r["n"] == 36000
    assert r["p95_s"] <= 15
    assert r["porcentaje_dentro_15s"] == 100
    assert r["drenaje_s"] < 15
    assert r["pendientes_fuera_plazo_por_minuto"] == [0] * 5


@pytest.mark.parametrize("aciertos", [0, .2, .8])
@pytest.mark.parametrize("semilla", [7, 19, 42])
def test_ff04_consultas_en_rafaga_y_cache_fria(aciertos, semilla):
    r = simular_consultas(tasa=5 * 50000 / 3600, aciertos=aciertos, semilla=semilla)
    assert r["p95_ms"] <= 2000


def test_controles_negativos_detectan_regresion_rendimiento():
    assert simular_ingesta("base")["p95_s"] > 15
    assert any(simular_ingesta("base")["pendientes_fuera_plazo_por_minuto"])
    assert simular_consultas("base")["p95_ms"] > 2000
    assert simular_consultas("solo_cache", aciertos=0)["p95_ms"] > 2000


def test_ff05_mapas_caidos_sin_pantallas_vacias():
    r = simular()
    assert r["pantallas_vacias"] == 0
    assert r["recuperacion_s"] <= 30
    assert r["llamadas_en_caida"] < simular("reintentos")["llamadas_en_caida"] / 5
    assert simular("base")["pantallas_vacias"] > 0


def test_ff06_cache_no_rejuvenece_lectura_obsoleta():
    reloj, repo = Reloj(), RepositorioMemoria()
    repo.guardar(LecturaETA("B", "P", 1, 0, 4))
    cache = ConCacheETA(repo, reloj)
    servicio = ConsultaSeguimiento(cache, reloj)
    reloj.ahora = 29.5
    assert servicio.consultar("B", "P").eta_min == 4
    reloj.ahora = 30.5  # El TTL aún no vence, pero la fuente ya es obsoleta.
    respuesta = servicio.consultar("B", "P")
    assert respuesta.eta_min is None
    assert respuesta.estado == "SIN_SEÑAL"


def test_ff07_dto_publico_sin_datos_personales():
    reloj, repo = Reloj(), RepositorioMemoria()
    vista = construir(repo, MapasSimulados(reloj), reloj)
    for i in range(100):
        repo.guardar(LecturaETA(str(i), "P", i, 0, 3))
        datos = consultar(vista, str(i), "P")["seguimiento"]
        assert set(datos) == {"bus_id", "paradero_id", "eta_min", "edad_s", "estado"}


def test_cache_ttl_clave_compuesta_y_datos_mas_recientes():
    reloj, repo = Reloj(), RepositorioMemoria()
    repo.guardar(LecturaETA("B", "P1", 1, 0, 4))
    repo.guardar(LecturaETA("B", "P2", 1, 0, 8))
    cache = ConCacheETA(repo, reloj, capacidad=2)
    assert cache.obtener("B", "P1").eta_min == 4
    assert cache.obtener("B", "P2").eta_min == 8
    assert cache.obtener("B", "P1").eta_min == 4
    assert repo.consultas == 2
    repo.guardar(LecturaETA("B", "P1", 2, 1, 2))
    reloj.ahora = 2
    assert cache.obtener("B", "P1").eta_min == 2
    assert not repo.guardar(LecturaETA("B", "P1", 1, 0, 99))
    assert not repo.guardar(LecturaETA("B", "P1", 3, 0, 99))


def test_cache_acotada_y_ausencia_no_cacheada():
    reloj, repo = Reloj(), RepositorioMemoria()
    cache = ConCacheETA(repo, reloj, capacidad=1)
    assert cache.obtener("B", "P") is None
    for i in range(3):
        repo.guardar(LecturaETA(str(i), "P", i, 0, 1))
        cache.obtener(str(i), "P")
    assert len(cache.cache) == 1
    with pytest.raises(ValueError):
        ConCacheETA(repo, reloj, ttl_s=30)


def test_lectura_futura_no_es_actual():
    reloj, repo = Reloj(), RepositorioMemoria()
    repo.guardar(LecturaETA("B", "P", 1, 10, 3))
    assert ConsultaSeguimiento(repo, reloj).consultar("B", "P").eta_min is None


def test_breaker_abre_sondea_reabre_y_recupera():
    reloj = Reloj()
    proveedor = MapasSimulados(reloj, inicio=0, fin=100)
    breaker = ConCircuitBreaker(proveedor, reloj)
    for _ in range(3):
        with pytest.raises(TimeoutError):
            breaker.obtener()
    assert breaker.estado == "ABIERTO"
    with pytest.raises(CircuitoAbierto):
        breaker.obtener()
    assert proveedor.llamadas_en_caida == 3
    reloj.ahora = 30
    assert breaker.estado == "SEMIABIERTO"
    with pytest.raises(TimeoutError):
        breaker.obtener()
    assert breaker.estado == "ABIERTO"
    reloj.ahora = 100
    assert breaker.obtener() == "tile-simulado"
    assert breaker.estado == "CERRADO"


def test_fallback_sin_lectura_y_con_lectura_vencida():
    reloj, repo = Reloj(), RepositorioMemoria()
    vista = construir(repo, MapasSimulados(reloj, 0, 100), reloj)
    assert consultar(vista, "B", "P")["seguimiento"]["estado"] == "SIN_DATOS"
    repo.guardar(LecturaETA("B", "P", 1, 0, 3))
    reloj.ahora = 40
    respuesta = consultar(vista, "B", "P")
    assert respuesta["aviso"]
    assert respuesta["seguimiento"]["estado"] == "SIN_SEÑAL"
    assert respuesta["seguimiento"]["eta_min"] is None
