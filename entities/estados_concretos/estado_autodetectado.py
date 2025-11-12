from entities.estado import Estado

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
        