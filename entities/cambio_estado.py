from datetime import datetime
from entities.estado import Estado

class CambioEstado:
    def __init__(self, fechaHoraInicio: datetime, estado: Estado, responsable: str):
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFin = None
        self.estado = estado
        self.responsable = responsable

    def setFechaHoraFin(self, fechaHoraFin: datetime):
        self.fechaHoraFin = fechaHoraFin

    def esEstadoActual(self) -> bool:
        return self.fechaHoraFin is None

    def esAutoDetectado(self) -> bool:
        return self.estado.esAutoDetectado()

    def esPendienteDeRevision(self) -> bool:
        return self.estado.esPendienteDeRevision()