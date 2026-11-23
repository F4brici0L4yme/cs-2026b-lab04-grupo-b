"""La prueba de ruta curva demuestra el defecto del borrador ingenuo."""
from lab12.evidencias.borrador_vago import eta_minutos


def test_estimacion_no_debe_usar_solo_distancia_en_linea_recta() -> None:
    # La ruta tiene ~2.08 km restantes; una cuerda de ~1.4 km subestima el ETA.
    eta_borrador = eta_minutos(1400, 10)
    eta_por_ruta = eta_minutos(2072, 10)
    assert eta_borrador >= eta_por_ruta
