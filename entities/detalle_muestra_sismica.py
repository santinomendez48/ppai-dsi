from entities.tipo_de_dato import TipoDeDato

class DetalleMuestraSismica:
    def __init__(self, valor: float, tipo: TipoDeDato):
        self.valor = valor
        self.tipoDeDato = tipo

    def getDatos(self):
        return {"valor": self.valor, "tipo": self.tipoDeDato.getDenominacion()}

    def getLongitudOnda(self):
        if self.tipoDeDato.esLongitudOnda():
            return self.valor
        return None
    
    def getFrecuenciaOnda(self):
        if self.tipoDeDato.esFrecuenciaOnda():
            return self.valor
        return None

    def getVelocidadOnda(self):
        if self.tipoDeDato.esVelocidadOnda():
            return self.valor
        return None