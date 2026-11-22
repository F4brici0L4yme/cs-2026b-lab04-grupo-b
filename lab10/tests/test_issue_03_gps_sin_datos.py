"""Regresión ISSUE-03: una lectura ausente no se anuncia como actual."""

from rutasit_demo import crear_respuesta_gps


def test_issue_03_gps_sin_lectura_devuelve_estado_sin_datos():
    assert crear_respuesta_gps(None) == {"eta_min": None, "estado": "SIN_DATOS"}
