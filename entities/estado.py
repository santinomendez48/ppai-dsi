from abc import ABC, abstractmethod
from datetime import datetime
from entities.evento_sismico import EventoSismico
from entities.cambio_estado import CambioEstado
from typing import List

class Estado(ABC):
    estados = []

    def __init__(self, nombreEstado: str, ambito: str):
        self.nombreEstado = nombreEstado
        self.ambito = ambito
        # Evitar duplicados en la lista de estados
        if not any(e.nombreEstado == nombreEstado for e in Estado.estados):
            Estado.estados.append(self)

    @classmethod
    def getEstadoPorNombre(cls, nombreEstado: str):
        for estado in cls.estados:
            if estado.nombreEstado == nombreEstado:
                return estado
        return None

    @abstractmethod
    def esAutoDetectado(self) -> bool:
        pass

    @abstractmethod
    def esPendienteDeRevision(self) -> bool:
        pass

    @abstractmethod
    def esBloqueadoEnRevision(self) -> bool:
        pass

    @abstractmethod
    def esEstadoRechazado(self) -> bool:
        pass
    
    @abstractmethod
    def bloquearEvento(self, evento: EventoSismico, fechaHoraFin: datetime, responsable: str, cambiosEstado: List[CambioEstado]):
        pass
