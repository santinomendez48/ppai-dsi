from datetime import datetime
from entities.evento_sismico import EventoSismico
from entities.clasificacion_sismo import ClasificacionSismo
from entities.origen_de_generacion import OrigenDeGeneracion
from entities.alcance_sismo import AlcanceSismo
from entities.serie_temporal import SerieTemporal
from entities.sismografo import Sismografo
from entities.estacion_sismologica import EstacionSismologica
from entities.muestra_sismica import MuestraSismica
from entities.tipo_de_dato import TipoDeDato
from entities.estado import Estado
from entities.sesion import Sesion
from entities.empleado import Empleado
from persistence.repositories.evento_sismico_repository import EventoSismicoRepository

# ===================== GESTOR =====================
class GestorRegistrarResultadoRevisionManual:
    def __init__(self):
        # Crear sesión de ejemplo
        empleado_ejemplo = Empleado("Juan", "Perez", "jperez@gmail.com", "3512345678")
        self.sesion = Sesion(empleado_ejemplo)
        self.repository = EventoSismicoRepository()
        self.eventos = []
        self.evento_seleccionado = None
        self.estacion_seleccionada = None
        self.empleado_logueado = None
    
    # Metodo para inicializar el gestor
    def registrarResultadoRevisionManual(self):
        # Cargar eventos desde la base de datos
        eventos_bd = self.repository.find_all()
        
        # Si no hay eventos en BD, crear eventos de ejemplo y guardarlos
        if eventos_bd:
            self.eventos = eventos_bd
        
        self.evento_seleccionado = None
        self.estacion_seleccionada = None

    # Metodo para buscar sismos autodetectados
    def buscarSismosAutodetectados(self):
        return [e for e in self.eventos if e.esAutodetectado()]

    # Metodo para tomar la seleccion del sismo
    def tomarSeleccionSismo(self, evento_id):
        for e in self.eventos:
            if e.id == evento_id:
                self.evento_seleccionado = e
                self.bloquearEventoSeleccionado()
                return e
        return None

    # Metodo para bloquear el evento seleccionado
    def bloquearEventoSeleccionado(self):
        if self.evento_seleccionado is not None:
            self.empleado_logueado = self.getASlogueado()
            fechaHoraActual = self.getFechaHoraActual()
            self.evento_seleccionado.bloquearEventoSismico(fechaHoraActual, self.empleado_logueado)
            print(f"Evento: {self.evento_seleccionado}")
        else:
            raise ValueError("No hay evento seleccionado para bloquear.")
        # Guardar cambios en la base de datos
        self.repository.update(self.evento_seleccionado)
        print("Evento bloqueado y guardado en la base de datos.")

    # Metodo para obtener los valores de las muestras
    def obtenerValoresMuestras(self, evento):
        return evento.obtenerValoresMuestras()

    # Metodo para modificar los datos del evento
    def modificarEvento(self, evento, magnitud, alcance, origen):
        evento.valorMagnitud = float(magnitud)
        evento.alcanceSismo = AlcanceSismo(alcance, "")
        evento.origenGeneracion = OrigenDeGeneracion(origen, "")
        # Guardar cambios en la base de datos
        self.repository.update(evento)

    # Metodo para confirmar el evento
    def confirmarEvento(self, evento):
        estado = self.getEstadoConfirmado()
        empleado = self.getASlogueado()
        fechaHoraActual = self.getFechaHoraActual()
        evento.confirmarEvento(estado, fechaHoraActual, empleado)
        # Guardar cambios en la base de datos
        self.repository.update(evento)

    # Metodo para rechazar el evento
    def rechazarEvento(self, evento):
        fechaHoraActual = self.getFechaHoraActual()
        self.evento_seleccionado.rechazarEvento(fechaHoraActual, self.getASlogueado())
        # Guardar cambios en la base de datos
        self.repository.update(evento)

    # Metodo para derivar el evento
    def derivarEvento(self, evento):
        estado = self.getEstadoDerivadoAExperto()
        empleado = self.getASlogueado()
        fechaHoraActual = self.getFechaHoraActual()
        evento.derivarExperto(estado, fechaHoraActual, empleado)
        # Guardar cambios en la base de datos
        self.repository.update(evento)

    # Metodo para obtener el estado "Derivado a Experto"
    def getEstadoDerivadoAExperto(self):
        estado = Estado.getEstadoPorNombre("DerivadoAExperto")
        if estado is None:
            raise ValueError("Estado 'DerivadoAExperto' no encontrado")
        return estado

    # Metodo para obtener el estado "Rechazado"
    def getEstadoRechazado(self):
        estado = Estado.getEstadoPorNombre("Rechazado")
        if estado is None:
            raise ValueError("Estado 'Rechazado' no encontrado")
        return estado

    # Metodo para obtener el estado "Confirmado"
    def getEstadoConfirmado(self):
        estado = Estado.getEstadoPorNombre("Confirmado")
        if estado is None:
            raise ValueError("Estado 'Confirmado' no encontrado")
        return estado

    # Metodo para obtener el Analista Sismológico logueado (simulado)
    def getASlogueado(self):
        return self.sesion.getEmpleado()

    # Metodo para obtener la fecha y hora actual
    def getFechaHoraActual(self):
        return datetime.now()

    # Metodo para obtener los datos del evento seleccionado 
    def buscarDatosEventoSeleccionado(self, evento: EventoSismico):
        datos = {}
        datos["Clasificacion"] = evento.getClasificacion()
        datos["Origen"] = evento.getOrigen()
        datos["Alcance"] = evento.getAlcance()
        return datos

