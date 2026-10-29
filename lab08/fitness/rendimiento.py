"""Colas FCFS multiserver con parámetros hipotéticos explícitos.

La optimización representa geometría precargada y reducción de trabajo repetido.
No se atribuyen tiempos medidos al prototipo en memoria ni al PostgreSQL real.
"""

import heapq
import math
import random
import statistics

SERVICIO_INGESTA_S = {"base": 0.022, "optimizada": 0.006}
SERVICIO_CONSULTA_S = {"base": 0.180, "indice": 0.025, "cache": 0.003}


def percentil(valores, q=0.95):
    ordenados = sorted(valores)
    return ordenados[max(0, math.ceil(q * len(ordenados)) - 1)]


def llegadas_poisson(tasa, segundos, semilla):
    rnd, t, llegadas = random.Random(semilla), 0.0, []
    while True:
        t += rnd.expovariate(tasa)
        if t >= segundos:
            return llegadas
        llegadas.append(t)


def cola(llegadas, servicio, workers=2, semilla=7):
    if not llegadas or workers < 1:
        raise ValueError("Se requieren llegadas y workers positivos")
    rnd, libres, respuestas, fines = random.Random(semilla), [0.0] * workers, [], []
    for llegada in sorted(llegadas):
        inicio = max(llegada, heapq.heappop(libres))
        fin = inicio + servicio(rnd)
        heapq.heappush(libres, fin)
        respuestas.append(fin - llegada)
        fines.append(fin)
    return respuestas, fines


def lognormal(rnd, media, sigma=0.35):
    return rnd.lognormvariate(math.log(media) - sigma * sigma / 2, sigma)


def simular_ingesta(modo="optimizada", buses=1200, segundos=300,
                     rafagas=False, semilla=7, factor_servicio=1.0):
    # Una lectura cada 10 s por bus; tanto fases uniformes como ráfaga sincronizada.
    rnd = random.Random(semilla)
    fases = [0.0 if rafagas else rnd.uniform(0, 10) for _ in range(buses)]
    capturas = sorted(fase + t for t in range(0, segundos, 10)
                      for fase in fases if fase + t < segundos)
    # Desorden de red no cambia el número de eventos. Sobrecosto conservador de
    # 200 ms de red, TTL máximo 2 s y presupuesto API 2 s sumado al procesamiento.
    servicio = lambda r: lognormal(r, SERVICIO_INGESTA_S[modo] * factor_servicio)
    duraciones, fines = cola(capturas, servicio, semilla=semilla)
    extremo = [r + 0.2 + 2 + 2 for r in duraciones]
    # QA-01 exige también que *todos* los eventos capturados en cada minuto
    # estén disponibles antes del cierre de ese minuto más 15 s. Esto es una
    # condición distinta del p95 y del backlog al cierre de los 300 s.
    completados_por_minuto = []
    for minuto in range(math.ceil(segundos / 60)):
        cierre = min((minuto + 1) * 60, segundos)
        pendientes = sum(captura >= minuto * 60 and captura < cierre
                         and captura + latencia > cierre + 15
                         for captura, latencia in zip(capturas, extremo))
        completados_por_minuto.append(pendientes)
    return {"n": len(capturas), "p95_s": percentil(extremo),
            "p95_procesamiento_s": percentil(duraciones), "max_s": max(extremo),
            "pendientes_al_cierre": sum(f > segundos for f in fines),
            "pendientes_fuera_plazo_por_minuto": completados_por_minuto,
            "porcentaje_dentro_15s": 100 * sum(r <= 15 for r in extremo) / len(extremo),
            "drenaje_s": max(0, max(fines) - segundos),
            "utilizacion_teorica": buses / 10 * SERVICIO_INGESTA_S[modo] * factor_servicio / 2}


def simular_consultas(modo="indice_cache", tasa=50000 / 3600, segundos=300,
                      aciertos=0.8, semilla=7, factor_servicio=1.0):
    if not 0 <= aciertos <= 1:
        raise ValueError("Aciertos fuera de [0, 1]")
    llegadas = llegadas_poisson(tasa, segundos, semilla)

    def servicio(rnd):
        usa_cache = modo in ("solo_cache", "indice_cache") and rnd.random() < aciertos
        base = "base" if modo in ("base", "solo_cache") else "indice"
        media = SERVICIO_CONSULTA_S["cache" if usa_cache else base]
        return lognormal(rnd, media * factor_servicio)

    respuestas, _ = cola(llegadas, servicio, semilla=semilla + 1)
    # 100 ms hipotéticos adicionales de transporte/serialización.
    ms = [(r + 0.1) * 1000 for r in respuestas]
    return {"n": len(ms), "p95_ms": percentil(ms), "p50_ms": percentil(ms, .50),
            "media_ms": statistics.mean(ms)}
