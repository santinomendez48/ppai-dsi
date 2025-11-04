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

# ===================== GESTOR =====================
class GestorRegistrarResultadoRevisionManual:
    def __init__(self):
        # Crear sesión de ejemplo
        empleado_ejemplo = Empleado("Juan", "Perez", "jperez@gmail.com", "3512345678")
        self.sesion = Sesion(empleado_ejemplo)
        self.eventos = []
        self.evento_seleccionado = None
        self.estacion_seleccionada = None
    
    def _crear_eventos_ejemplo(self):
        # Datos de ejemplo
        clasif1 = ClasificacionSismo("Superficial", 0, 70)
        origen1 = OrigenDeGeneracion("Interplaca", "Entre placas")
        alcance1 = AlcanceSismo("Local", "Afecta zona local")
        clasif2 = ClasificacionSismo("Intermedio", 70, 300)
        origen2 = OrigenDeGeneracion("Intraplaca", "Dentro de placa")
        alcance2 = AlcanceSismo("Regional", "Afecta zona regional")
        estacion1 = EstacionSismologica("E1", "Doc1", "2025-01-01", -31.42, -64.18, "Córdoba", "Cert1")
        estacion2 = EstacionSismologica("E2", "Doc2", "2025-01-01", -31.43, -64.19, "Mendoza", "Cert2")
        sismografo1 = Sismografo("2025-01-01", "S1", "SN1", estacion1)
        sismografo2 = Sismografo("2025-01-01", "S2", "SN2", estacion2)
        # Serie y muestras para estación 1
        serie1 = SerieTemporal(datetime(2025, 7, 3, 22, 8), 1.0, False, sismografo1)
        tipo_vel = TipoDeDato("Velocidad de Onda", "m/s", 0)
        tipo_frec = TipoDeDato("Frecuencia de Onda", "Hz", 0)
        tipo_long = TipoDeDato("Longitud de Onda", "m", 0)
        for i in range(5):
            muestra = MuestraSismica(datetime(2025, 7, 3, 22, 8))
            muestra.crearDetalleMuestra(1.5 + i, tipo_vel)
            muestra.crearDetalleMuestra(8.67 + i, tipo_frec)
            muestra.crearDetalleMuestra(17.75 + i, tipo_long)
            serie1.muestrasSismicas.append(muestra)
        # Serie y muestras para estación 2 (datos diferentes)
        serie2 = SerieTemporal(datetime(2025, 7, 3, 22, 8), 1.0, False, sismografo2)
        for i in range(5):
            muestra = MuestraSismica(datetime(2025, 7, 3, 22, 8))
            muestra.crearDetalleMuestra(2.0 + i, tipo_vel)
            muestra.crearDetalleMuestra(9.0 + i, tipo_frec)
            muestra.crearDetalleMuestra(18.0 + i, tipo_long)
            serie2.muestrasSismicas.append(muestra)
        evento1 = EventoSismico(1, datetime(2025, 7, 3, 22, 8), -31.42, -64.18, -31.43, -64.19, 4.3, clasif1, origen1, alcance1)
        estado_auto = Estado.getEstadoPorNombre("AutoDetectado")
        if estado_auto is None:
            raise ValueError("Estado 'AutoDetectado' no encontrado")
        evento1.crearCambioEstado(estado_auto, self.getFechaHoraActual(), self.getASlogueado())
        evento1.seriesTemporales = [serie1, serie2]
        evento2 = EventoSismico(2, datetime(2025, 7, 3, 21, 48), -31.43, -64.19, -31.44, -64.20, 6.1, clasif2, origen2, alcance2)
        evento2.crearCambioEstado(estado_auto, self.getFechaHoraActual(), self.getASlogueado())
        evento2.seriesTemporales = [serie1, serie2]
        return [evento1, evento2]

    # Metodo para inicializar el gestor
    def registrarResultadoRevisionManual(self):
        self.eventos = self._crear_eventos_ejemplo()
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
                return e
        return None

    # Metodo para bloquear el evento seleccionado
    def bloquearEventoSeleccionado(self):
        if self.evento_seleccionado is not None:
            estado_bloqueado = self.getEstadoBloqueadoEnRevision()
            empleado = self.getASlogueado()
            fechaHoraActual = self.getFechaHoraActual()
            self.evento_seleccionado.bloquearEventoSismico(estado_bloqueado, fechaHoraActual, empleado)
        else:
            raise ValueError("No hay evento seleccionado para bloquear.")

    # Metodo para obtener el estado bloqueado en revision
    def getEstadoBloqueadoEnRevision(self):
        estado = Estado.getEstadoPorNombre("BloqueadoEnRevision")
        if estado is None:
            raise ValueError("Estado 'Bloqueado' no encontrado")
        return estado

    # Metodo para obtener los valores de las muestras
    def obtenerValoresMuestras(self, evento):
        return evento.obtenerValoresMuestras()

    # Metodo para modificar los datos del evento
    def modificarEvento(self, evento, magnitud, alcance, origen):
        evento.valorMagnitud = float(magnitud)
        evento.alcanceSismo = AlcanceSismo(alcance, "")
        evento.origenGeneracion = OrigenDeGeneracion(origen, "")

    # Metodo para confirmar el evento
    def confirmarEvento(self, evento):
        estado = self.getEstadoConfirmado()
        empleado = self.getASlogueado()
        fechaHoraActual = self.getFechaHoraActual()
        evento.confirmarEvento(estado, fechaHoraActual, empleado)

    # Metodo para rechazar el evento
    def rechazarEvento(self, evento):
        estado = self.getEstadoRechazado()
        empleado = self.getASlogueado()
        fechaHoraActual = self.getFechaHoraActual()
        evento.rechazarEvento(estado, fechaHoraActual, empleado)

    # Metodo para derivar el evento
    def derivarEvento(self, evento):
        estado = self.getEstadoDerivadoAExperto()
        empleado = self.getASlogueado()
        fechaHoraActual = self.getFechaHoraActual()
        evento.derivarExperto(estado, fechaHoraActual, empleado)

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

