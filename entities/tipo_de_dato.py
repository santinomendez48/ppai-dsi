class TipoDeDato:
    def __init__(self, denominacion: str, nombreUnidadMedida: str, valorUmbral: float):
        self.denominacion = denominacion
        self.nombreUnidadMedida = nombreUnidadMedida
        self.valorUmbral = valorUmbral

    def getDenominacion(self) -> str:
        return self.denominacion

    def esLongitudOnda(self) -> bool:
        if self.denominacion == "Longitud de Onda":
            return True
        return False

    def esFrecuenciaOnda(self) -> bool:
        if self.denominacion == "Frecuencia de Onda":
            return True
        return False

    def esVelocidadOnda(self) -> bool:
        if self.denominacion == "Velocidad de Onda":
            return True
        return False