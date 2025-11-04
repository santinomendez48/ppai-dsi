class AlcanceSismo:
    def __init__(self, nombre: str, descripcion: str):
        self.nombre = nombre
        self.descripcion = descripcion

    def getNombre(self) -> str:
        return self.nombre