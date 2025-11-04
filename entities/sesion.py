from entities.empleado import Empleado

class Sesion:
    def __init__(self, empleado: Empleado):
        self.empleado = empleado

    def getEmpleado(self) -> str:
        return self.empleado.getNombre()