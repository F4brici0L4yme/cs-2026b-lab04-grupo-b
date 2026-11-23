"""Casos de uso y adaptadores de presentación mínimos para RutaSIT."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from .compartido import Id
from .dominio import (
    AlertaDesvio,
    Bus,
    ETA,
    EstadoBus,
    Paradero,
    Ruta,
    UbicacionGPS,
)
from .puertos import IEstimadorETA, IGpsProvider, INotificadorAlerta, IRepositorioRutaSIT, IReloj

ANTIGUEDAD_MAX_TELEMETRIA = timedelta(seconds=30)
TOLERANCIA_DESVIO_M = 30.0
TOLERANCIA_PARADERO_M = 15.0


@dataclass(frozen=True, slots=True)
class ResultadoSeguimiento:
    bus_id: Id
    estado: EstadoBus
    ubicacion: UbicacionGPS | None
    eta: ETA | None
    alerta: AlertaDesvio | None
    telemetria_vigente: bool


class SeguimientoService:
    def __init__(
        self,
        repositorio: IRepositorioRutaSIT,
        gps_provider: IGpsProvider,
        notificador: INotificadorAlerta,
        estimador_eta: IEstimadorETA,
        reloj: IReloj,
    ) -> None:
        self._repositorio = repositorio
        self._gps_provider = gps_provider
        self._notificador = notificador
        self._estimador_eta = estimador_eta
        self._reloj = reloj

    def consultar_seguimiento(self, bus_id: Id, paradero_id: Id) -> ResultadoSeguimiento:
        bus = self._repositorio.obtener_bus(bus_id)
        if bus.estado_actual() is EstadoBus.FUERA_DE_SERVICIO:
            return ResultadoSeguimiento(
                bus_id=bus.id,
                estado=bus.estado_actual(),
                ubicacion=bus.ultima_ubicacion,
                eta=None,
                alerta=None,
                telemetria_vigente=False,
            )
        if bus.ruta_id is None:
            raise ValueError(f"El bus {bus_id} no tiene ruta asignada")
        ruta = self._repositorio.obtener_ruta(bus.ruta_id)
        paradero = self._repositorio.obtener_paradero(paradero_id)
        ubicacion = self._gps_provider.obtener_ultima_ubicacion(bus_id)
        return self._evaluar_posicion(bus, ruta, paradero, ubicacion)

    def procesar_telemetria(self, bus_id: Id, ubicacion: UbicacionGPS) -> ResultadoSeguimiento:
        bus = self._repositorio.obtener_bus(bus_id)
        if bus.ruta_id is None:
            raise ValueError(f"El bus {bus_id} no tiene ruta asignada")
        ruta = self._repositorio.obtener_ruta(bus.ruta_id)
        paradero = ruta.siguiente_paradero(ubicacion)
        return self._evaluar_posicion(bus, ruta, paradero, ubicacion)

    def calcular_eta(
        self,
        bus: Bus,
        paradero: Paradero,
        calculada_en: datetime,
    ) -> ETA | None:
        return self._estimador_eta.calcular_eta(bus, paradero, calculada_en)

    def _evaluar_posicion(
        self,
        bus: Bus,
        ruta: Ruta,
        paradero: Paradero | None,
        ubicacion: UbicacionGPS,
    ) -> ResultadoSeguimiento:
        if bus.estado_actual() is EstadoBus.FUERA_DE_SERVICIO:
            return ResultadoSeguimiento(
                bus_id=bus.id,
                estado=bus.estado_actual(),
                ubicacion=bus.ultima_ubicacion,
                eta=None,
                alerta=None,
                telemetria_vigente=False,
            )
        ahora = self._reloj.ahora()
        if not ubicacion.es_reciente(ahora, ANTIGUEDAD_MAX_TELEMETRIA):
            return ResultadoSeguimiento(
                bus_id=bus.id,
                estado=bus.estado_actual(),
                ubicacion=bus.ultima_ubicacion,
                eta=None,
                alerta=None,
                telemetria_vigente=False,
            )

        estado_anterior = bus.estado_actual()
        bus.actualizar_ubicacion(ubicacion)
        eta_candidato = None
        if estado_anterior in (EstadoBus.EN_RUTA, EstadoBus.EN_PARADERO, EstadoBus.DESVIADO) and paradero is not None:
            eta_candidato = self.calcular_eta(bus, paradero, ahora)
        estado = bus.actualizar_estado_por_ubicacion(
            ruta,
            paradero,
            TOLERANCIA_DESVIO_M,
            TOLERANCIA_PARADERO_M,
        )

        alerta: AlertaDesvio | None = None
        eta = None
        if estado is EstadoBus.DESVIADO:
            if estado_anterior is not EstadoBus.DESVIADO:
                alerta = AlertaDesvio.desde_bus(bus, ubicacion, ahora)
                self._notificador.notificar(alerta)
        elif estado in (EstadoBus.EN_RUTA, EstadoBus.EN_PARADERO):
            eta = eta_candidato

        self._repositorio.guardar_bus(bus)
        return ResultadoSeguimiento(
            bus_id=bus.id,
            estado=estado,
            ubicacion=ubicacion,
            eta=eta,
            alerta=alerta,
            telemetria_vigente=True,
        )


class MonitoreoController:
    def __init__(self, seguimiento: SeguimientoService) -> None:
        self._seguimiento = seguimiento

    def consultar_seguimiento(self, bus_id: Id, paradero_id: Id) -> ResultadoSeguimiento:
        return self._seguimiento.consultar_seguimiento(bus_id, paradero_id)


class RutaSITAPI:
    """Fachada HTTP simplificada; el transporte real se define fuera del dominio."""

    def __init__(self, controller: MonitoreoController) -> None:
        self._controller = controller

    def consultar_seguimiento(self, bus_id: Id, paradero_id: Id) -> ResultadoSeguimiento:
        return self._controller.consultar_seguimiento(bus_id, paradero_id)
