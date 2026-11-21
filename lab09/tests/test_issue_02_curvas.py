"""Regresión ISSUE-02: la posición se compara con segmentos, no solo hitos."""

from rutasit_demo import Punto, esta_en_ruta


def test_issue_02_detecta_bus_sobre_tramo_curvo_entre_puntos():
    trazado = (Punto(0, 0), Punto(50, 0), Punto(50, 50))
    bus = Punto(25, 5)

    assert esta_en_ruta(bus, trazado, tolerancia_m=10)


def test_issue_02_rechaza_posicion_lejos_del_trazado_curvo():
    trazado = (Punto(0, 0), Punto(50, 0), Punto(50, 50))
    bus = Punto(25, 40)

    assert not esta_en_ruta(bus, trazado, tolerancia_m=10)


def test_issue_02_ignora_waypoints_repetidos_al_calcular_segmentos():
    trazado = (Punto(0, 0), Punto(0, 0), Punto(100, 0))

    assert esta_en_ruta(Punto(50, 5), trazado, tolerancia_m=10)
