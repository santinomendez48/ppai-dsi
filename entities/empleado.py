class Empleado:
    def __init__(self, nombre: str, apellido: str, mail: str, telefono: str):
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.telefono = telefono

    def obtenerMail(self) -> str:
        return self.mail

    def getNombre(self) -> str:
        return f"{self.nombre} {self.apellido}"