from entities.estado import Estado
from entities.evento_sismico import EventoSismico
from datetime import datetime
from typing import List
from entities.cambio_estado import CambioEstado

class PendienteRevision(Estado):
    def __init__(self):
        super().__init__("PendienteRevision", "Pendiente de revisión")

    def esAutoDetectado(self) -> bool:
        return False

    def esPendienteDeRevision(self) -> bool:
        return True

    def esBloqueadoEnRevision(self) -> bool:
        return False

    def esEstadoRechazado(self) -> bool:
        return False
    
    def bloquearEvento(self, evento: EventoSismico, fechaHoraActual: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        cambioActual = self.buscarCambioEstadoActual(cambiosEstado)
        if cambioActual is not None:
            cambioActual.setFechaHoraFin(fechaHoraActual)
            nuevoEstado = self.crearEstadoBloqueadoEnRevision()
            nuevoCambio = self.crearCambioEstado(fechaHoraActual, nuevoEstado, responsable)
            evento.agregarCambioEstado(nuevoCambio)
            evento.setEstadoActual(nuevoEstado)
        else:
            raise ValueError("Error al bloquear evento: no hay cambio de estado actual para bloquear.")

    def buscarCambioEstadoActual(self, cambiosEstado: List[CambioEstado]) -> CambioEstado:
        for cambio in cambiosEstado:
            if cambio.esEstadoActual():
                return cambio
        return None
    
    def crearEstadoBloqueadoEnRevision() -> Estado:
        return Estado.getEstadoPorNombre("BloqueadoEnRevision")

    def crearCambioEstado(self, fechaHoraInicio: datetime, nuevoEstado: Estado, responsable: str) -> CambioEstado:
        return CambioEstado(fechaHoraInicio, nuevoEstado, responsable)