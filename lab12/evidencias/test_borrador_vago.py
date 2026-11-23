"""La prueba de ruta curva demuestra el defecto del borrador ingenuo."""
from lab12.evidencias.borrador_vago import eta_minutos
from rutasit.dominio import UbicacionGPS
from rutasit_lab12.eta_ruta import distancia_restante_m
from datetime import datetime, timezone


def test_estimacion_no_debe_usar_solo_distancia_en_linea_recta() -> None:
    # La ruta tiene ~2.08 km restantes; una cuerda de ~1.4 km subestima el ETA.
    eta_borrador = eta_minutos(1400, 10)
    eta_por_ruta = eta_minutos(2072, 10)
    assert eta_borrador >= eta_por_ruta


def test_estimacion_final_pasa_el_mismo_criterio_de_ruta_curva() -> None:
    ahora = datetime(2026, 11, 23, tzinfo=timezone.utc)
    ruta = (
        UbicacionGPS(-16.4, -71.54, ahora),
        UbicacionGPS(-16.4, -71.53, ahora),
        UbicacionGPS(-16.39, -71.53, ahora),
    )
    actual = UbicacionGPS(-16.4, -71.539, ahora)
    paradero = UbicacionGPS(-16.39, -71.53, ahora)
    distancia = distancia_restante_m(ruta, actual, paradero)

    assert eta_minutos(distancia, 10) == 4
