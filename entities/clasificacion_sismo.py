class ClasificacionSismo:
    def __init__(self, nombre: str, kmProfundidadDesde: float, kmProfundidadHasta: float):
        self.nombre = nombre
        self.kmProfundidadDesde = kmProfundidadDesde
        self.kmProfundidadHasta = kmProfundidadHasta

    def getNombre(self) -> str:
        return self.nombre