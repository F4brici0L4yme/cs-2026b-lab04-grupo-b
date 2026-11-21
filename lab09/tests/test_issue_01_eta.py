"""Regresión ISSUE-01: un bus que pasó el paradero no puede tener ETA negativa."""

from rutasit_demo import calcular_eta_minutos


def test_issue_01_eta_no_es_negativa_si_el_bus_paso_el_paradero():
    assert calcular_eta_minutos(-120, 8.33) == 0
