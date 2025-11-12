from entities.estado import Estado

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