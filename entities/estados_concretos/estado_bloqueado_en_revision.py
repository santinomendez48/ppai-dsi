from typing import List
import datetime
from entities.cambio_estado import CambioEstado
from entities.estado import Estado
from entities.evento_sismico import EventoSismico

class BloqueadoEnRevision(Estado):
    def __init__(self):
        super().__init__("BloqueadoEnRevision", "Evento bloqueado para revisión")

    def esAutoDetectado(self) -> bool:
        return False

    def esPendienteDeRevision(self) -> bool:
        return False

    def esBloqueadoEnRevision(self) -> bool:
        return True

    def esEstadoRechazado(self) -> bool:
        return False

    def buscarCambioEstadoActual(self, cambiosEstado: List[CambioEstado]) -> CambioEstado:
        for cambio in cambiosEstado:
            if cambio.esEstadoActual():
                return cambio
        return None
    
    def crearCambioEstado(self, fechaHoraInicio: datetime, nuevoEstado: Estado, responsable: str) -> CambioEstado:
        return CambioEstado(fechaHoraInicio, nuevoEstado, responsable)
    
    def crearEstadoRechazado(self) -> Estado:
        return Estado.getEstadoPorNombre("Rechazado")
    
    def crearEstadoConfirmado(self) -> Estado:
        return Estado.getEstadoPorNombre("Confirmado")
    
    def crearEstadoDerivadoExperto(self) -> Estado:
        return Estado.getEstadoPorNombre("DerivadoAExperto")
    
    def rechazarEvento(self, evento: EventoSismico, fechaHoraActual: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        cambioActual = self.buscarCambioEstadoActual(cambiosEstado)
        if cambioActual is not None:
            cambioActual.setFechaHoraFin(fechaHoraActual)
            nuevoEstado = self.crearEstadoRechazado()
            nuevoCambio = self.crearCambioEstado(fechaHoraActual, nuevoEstado, responsable)
            evento.agregarCambioEstado(nuevoCambio)
            evento.setEstadoActual(nuevoEstado)
        else:
            raise ValueError("Error al rechazar evento: no hay cambio de estado actual para rechazar.")
    
    def confirmarEvento(self, evento: EventoSismico, fechaHoraActual: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        cambioActual = self.buscarCambioEstadoActual(cambiosEstado)
        if cambioActual is not None:
            cambioActual.setFechaHoraFin(fechaHoraActual)
            nuevoEstado = self.crearEstadoConfirmado()
            nuevoCambio = self.crearCambioEstado(fechaHoraActual, nuevoEstado, responsable)
            evento.agregarCambioEstado(nuevoCambio)
            evento.setEstadoActual(nuevoEstado)
        else:
            raise ValueError("Error al confirmar evento: no hay cambio de estado actual para confirmar.")
    
    def derivarExperto(self, evento: EventoSismico, fechaHoraActual: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        cambioActual = self.buscarCambioEstadoActual(cambiosEstado)
        if cambioActual is not None:
            cambioActual.setFechaHoraFin(fechaHoraActual)
            nuevoEstado = self.crearEstadoDerivadoExperto()
            nuevoCambio = self.crearCambioEstado(fechaHoraActual, nuevoEstado, responsable)
            evento.agregarCambioEstado(nuevoCambio)
            evento.setEstadoActual(nuevoEstado)
        else:
            raise ValueError("Error al derivar evento: no hay cambio de estado actual para derivar.")

    def bloquearEvento(self, evento: EventoSismico, fechaHoraActual: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        pass