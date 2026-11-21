import json

from agentes.metricas import medir_trazas


def test_metricas_cuenta_bloqueo_rechazo_y_contexto(tmp_path):
    archivo = tmp_path / "ejecucion.jsonl"
    eventos = [
        {"paso": 1, "estado": "CONTRATO_INVALIDO", "bloqueada": True},
        {
            "paso": 2,
            "estado": "BLOQUEADO",
            "accion": "ejecutar_comando",
            "bloqueada": True,
        },
        {
            "paso": 3,
            "estado": "FINALIZADO",
            "contexto_caracteres": 125,
            "texto": "ok",
        },
    ]
    archivo.write_text(
        "".join(json.dumps(evento) + "\n" for evento in eventos),
        encoding="utf-8",
    )
    resultado = medir_trazas([archivo])
    assert resultado["pasos"] == 3
    assert resultado["decisiones_rechazadas_contrato"] == 1
    assert resultado["acciones_bloqueadas"] == 1
    assert resultado["contexto_final_caracteres"] == 125
