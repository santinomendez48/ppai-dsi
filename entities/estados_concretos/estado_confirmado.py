from entities.estado import Estado

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