from datetime import datetime
from typing import List
from entities.detalle_muestra_sismica import DetalleMuestraSismica
from entities.tipo_de_dato import TipoDeDato

class MuestraSismica:
    def __init__(self, fechaHoraMuestra: datetime):
        self.fechaHoraMuestra = fechaHoraMuestra
        self.detalleMuestraSismica = []

    def crearDetalleMuestra(self, valor: float, tipo: TipoDeDato):
        detalle = DetalleMuestraSismica(valor, tipo)
        self.detalleMuestraSismica.append(detalle)

    def getDatosMuestras(self):
        datos = {
            'Instante': self.fechaHoraMuestra,
            'Longitud de Onda': None,
            'Frecuencia de Onda': None,
            'Velocidad de Onda': None
        }
        for detalle in self.detalleMuestraSismica:
            if detalle.getLongitudOnda() is not None:
                datos['Longitud de Onda'] = detalle.getLongitudOnda()
            if detalle.getFrecuenciaOnda() is not None:
                datos['Frecuencia de Onda'] = detalle.getFrecuenciaOnda()
            if detalle.getVelocidadOnda() is not None:
                datos['Velocidad de Onda'] = detalle.getVelocidadOnda()
        return datos
        