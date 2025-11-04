from datetime import datetime
from typing import List
from entities.muestra_sismica import MuestraSismica
from entities.sismografo import Sismografo

class SerieTemporal:
    def __init__(self, fechaHoraInicio: datetime, frecuenciaMuestreo: float, condicionAlarma: bool, sismografo: Sismografo):
        self.fechaHoraInicio = fechaHoraInicio
        self.frecuenciaMuestreo = frecuenciaMuestreo
        self.condicionAlarma = condicionAlarma
        self.sismografo = sismografo
        self.muestrasSismicas = []

    def obtenerValoresMuestras(self) -> list:
        return [m.getDatosMuestras() for m in self.muestrasSismicas]

    def getEstacionSismologica(self):
        return self.sismografo.getEstacionSismologica()