from datetime import datetime
from typing import List
from entities.cambio_estado import CambioEstado
from entities.serie_temporal import SerieTemporal
from entities.clasificacion_sismo import ClasificacionSismo
from entities.origen_de_generacion import OrigenDeGeneracion
from entities.alcance_sismo import AlcanceSismo
from entities.estado import Estado

class EventoSismico:
    def __init__(self, id: int, fechaHoraConcurrencia: datetime, latitudEpicentro: float, longitudEpicentro: float,
                 latitudHipocentro: float, longitudHipocentro: float, valorMagnitud: float,
                 clasificacion: ClasificacionSismo, origenGeneracion: OrigenDeGeneracion, alcanceSismo: AlcanceSismo):
        self.id = id
        self.fechaHoraConcurrencia = fechaHoraConcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.longitudEpicentro = longitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudHipocentro = longitudHipocentro
        self.valorMagnitud = valorMagnitud
        self.clasificacion = clasificacion
        self.origenGeneracion = origenGeneracion
        self.alcanceSismo = alcanceSismo
        self.seriesTemporales: List[SerieTemporal] = []
        self.cambiosEstado: List[CambioEstado] = []
        self.fechaHoraFin = None

    def crearCambioEstado(self, nuevo_estado: Estado, fecha_hora: datetime, responsable: str):
        # Buscar el primer cambio de estado actual (sin fechaHoraFin) y cerrarlo
        for cambio in self.cambiosEstado:
            if cambio.fechaHoraFin is None:
                cambio.setFechaHoraFin(fecha_hora)
                break
        cambio_nuevo = CambioEstado(fecha_hora, nuevo_estado, responsable)
        self.cambiosEstado.append(cambio_nuevo)

    def bloquearEventoSismico(self, estado, fechaHoraFin: datetime, responsable: str):
        self.crearCambioEstado(estado, fechaHoraFin, responsable)

    def rechazarEvento(self, estado, fechaHoraFin: datetime, responsable: str):
        self.crearCambioEstado(estado, fechaHoraFin, responsable)

    def confirmarEvento(self, estado, fechaHoraFin: datetime, responsable: str):
        self.crearCambioEstado(estado, fechaHoraFin, responsable)

    def derivarExperto(self, estado, fechaHoraFin: datetime, responsable: str):
        self.crearCambioEstado(estado, fechaHoraFin, responsable)

    def getAlcance(self) -> str:
        return self.alcanceSismo.getNombre()

    def getClasificacion(self) -> str:
        return self.clasificacion.getNombre()

    def getOrigen(self) -> str:
        return self.origenGeneracion.getNombre()

    def esAutodetectado(self) -> bool:
        if not self.cambiosEstado:
            return False
        ultimo_cambio = None
        for cambio in self.cambiosEstado:
            if cambio.fechaHoraFin is None:
                ultimo_cambio = cambio
                break
        return ultimo_cambio.esAutoDetectado() or ultimo_cambio.esPendienteDeRevision()

    def obtenerValoresMuestras(self) -> list:
        resultados = []
        for serie in self.seriesTemporales:
            nombre_estacion = serie.getEstacionSismologica().getNombre()
            for muestra in serie.obtenerValoresMuestras():
                resultados.append({
                    'Estacion Sismologica': nombre_estacion,
                    **muestra
                })
        return resultados