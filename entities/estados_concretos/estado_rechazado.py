from entities.estado import Estado
from typing import List
import datetime
from entities.cambio_estado import CambioEstado
from entities.evento_sismico import EventoSismico

class Rechazado(Estado):
    def __init__(self):
        super().__init__("Rechazado", "Evento rechazado por analista")

    def esAutoDetectado(self) -> bool:
        return False

    def esPendienteDeRevision(self) -> bool:
        return False

    def esBloqueadoEnRevision(self) -> bool:
        return False

    def esEstadoRechazado(self) -> bool:
        return True
    
    def bloquearEvento(self, evento: EventoSismico, fechaHoraFin: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        pass