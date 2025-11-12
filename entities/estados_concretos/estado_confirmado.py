from typing import List
import datetime
from entities.cambio_estado import CambioEstado
from entities.estado import Estado
from entities.evento_sismico import EventoSismico

class Confirmado(Estado):
    def __init__(self):
        super().__init__("Confirmado", "Evento confirmado por analista")

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