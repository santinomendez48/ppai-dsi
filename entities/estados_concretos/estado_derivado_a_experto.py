import datetime
from typing import List
from entities.cambio_estado import CambioEstado
from entities.estado import Estado
from entities.evento_sismico import EventoSismico

class DerivadoAExperto(Estado):
    def __init__(self):
        super().__init__("DerivadoAExperto", "Evento derivado a experto")

    def esAutoDetectado(self) -> bool:
        return False

    def esPendienteDeRevision(self) -> bool:
        return False

    def esBloqueadoEnRevision(self) -> bool:
        return False

    def esEstadoRechazado(self) -> bool:
        return False

    def bloquearEvento(self, evento: EventoSismico, fechaHoraFin: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        pass

    def rechazarEvento(self, evento: EventoSismico, fechaHoraActual: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        pass

    def confirmarEvento(self, evento: EventoSismico, fechaHoraActual: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        pass

    def derivarExperto(self, evento: EventoSismico, fechaHoraActual: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        pass