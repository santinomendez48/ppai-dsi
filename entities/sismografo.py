from entities.estacion_sismologica import EstacionSismologica

class Sismografo:
    def __init__(self, fechaAquisicion: str, identificadorSismografo: str, nroSerie: str, estacionSismologica: EstacionSismologica):
        self.fechaAdquisicion = fechaAquisicion
        self.identificadorSismografo = identificadorSismografo
        self.nroSerie = nroSerie
        self.estacionSismologica = estacionSismologica

    def getIdentificadorSismografo(self) -> str:
        return self.identificadorSismografo

    def getEstacionSismologica(self) -> EstacionSismologica:
        return self.estacionSismologica