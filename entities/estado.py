class Estado:
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

    def esAutoDetectado(self) -> bool:
        return self.nombreEstado == "AutoDetectado"

    def esPendienteDeRevision(self) -> bool:
        return self.nombreEstado == "PendienteRevision"

    def esBloqueadoEnRevision(self) -> bool:
        return self.nombreEstado == "BloqueadoEnRevision"

    def esEstadoRechazado(self) -> bool:
        return self.nombreEstado == "Rechazado"

# Estados hardcodeados
Estado("AutoDetectado", "Evento auto detectado")
Estado("PendienteRevision", "Pendiente de revisión")
Estado("BloqueadoEnRevision", "Evento bloqueado para revisión")
Estado("Rechazado", "Evento rechazado por analista")
Estado("Confirmado", "Evento confirmado por analista")
Estado("DerivadoAExperto", "Evento derivado a experto")
