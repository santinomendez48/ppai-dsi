from typing import List
import datetime
from entities.cambio_estado import CambioEstado
from entities.estado import Estado
from entities.evento_sismico import EventoSismico

class AutoDetectado(Estado):
    def __init__(self):
        super().__init__("AutoDetectado", "Evento auto detectado")

    def esAutoDetectado(self) -> bool:
        return True

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

    
        