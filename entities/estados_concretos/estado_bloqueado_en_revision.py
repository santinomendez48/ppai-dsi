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
    
    def bloquearEvento(self, evento: EventoSismico, fechaHoraFin: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        pass