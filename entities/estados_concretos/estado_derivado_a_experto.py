from entities.estado import Estado

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