from typing import List, Optional
from datetime import datetime
from persistence.database import Database
from persistence.repositories.base_repository import BaseRepository
from entities.evento_sismico import EventoSismico
from entities.clasificacion_sismo import ClasificacionSismo
from entities.origen_de_generacion import OrigenDeGeneracion
from entities.alcance_sismo import AlcanceSismo
from entities.estado import Estado
from entities.cambio_estado import CambioEstado
from entities.serie_temporal import SerieTemporal
from entities.sismografo import Sismografo
from entities.estacion_sismologica import EstacionSismologica
from entities.muestra_sismica import MuestraSismica
from entities.detalle_muestra_sismica import DetalleMuestraSismica
from entities.tipo_de_dato import TipoDeDato
from entities.estados_concretos.estado_autodetectado import AutoDetectado
from entities.estados_concretos.estado_confirmado import Confirmado
from entities.estados_concretos.estado_rechazado import Rechazado
from entities.estados_concretos.estado_derivado_a_experto import DerivadoAExperto
from entities.estados_concretos.estado_bloqueado_en_revision import BloqueadoEnRevision
from entities.estados_concretos.estado_pendiente_revision import PendienteRevision

class EventoSismicoRepository(BaseRepository[EventoSismico]):
    def __init__(self):
        self.db = Database()
        self._load_reference_data()
    
    def _load_reference_data(self):
        """Carga datos de referencia necesarios (estados, clasificaciones, etc.)"""
        # Inicializar todos los estados para que estén disponibles
        AutoDetectado()
        Confirmado()
        Rechazado()
        DerivadoAExperto()
        BloqueadoEnRevision()
        PendienteRevision()
        
        # Sincronizar estados con la BD
        self._sync_estados()
    
    def _sync_estados(self):
        """Sincroniza los estados en memoria con la BD"""
        for estado in Estado.estados:
            self._save_estado(estado)
    
    def save(self, evento: EventoSismico) -> EventoSismico:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Guardar clasificación si no existe
        clasif_id = self._save_clasificacion(evento.clasificacion)
        origen_id = self._save_origen(evento.origenGeneracion)
        alcance_id = self._save_alcance(evento.alcanceSismo)
        estado_actual_id = self._save_estado(evento.estadoActual)
        
        # Guardar evento
        cursor.execute('''
            INSERT INTO eventos_sismicos 
            (fecha_hora_concurrencia, latitud_epicentro, longitud_epicentro,
             latitud_hipocentro, longitud_hipocentro, valor_magnitud,
             clasificacion_id, origen_generacion_id, alcance_sismo_id, estado_actual_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            evento.fechaHoraConcurrencia.isoformat(),
            evento.latitudEpicentro,
            evento.longitudEpicentro,
            evento.latitudHipocentro,
            evento.longitudHipocentro,
            evento.valorMagnitud,
            clasif_id,
            origen_id,
            alcance_id,
            estado_actual_id
        ))
        
        evento_id = cursor.lastrowid
        evento.id = evento_id
        
        # Guardar cambios de estado
        for cambio in evento.cambiosEstado:
            self._save_cambio_estado(cambio, evento_id)
        
        # Guardar series temporales
        for serie in evento.seriesTemporales:
            self._save_serie_temporal(serie, evento_id)
        
        conn.commit()
        return evento
    
    def find_by_id(self, id: int) -> Optional[EventoSismico]:
        row = self.db.fetch_one('''
            SELECT e.*, c.nombre as clasificacion_nombre, c.km_profundidad_desde, c.km_profundidad_hasta,
                   o.nombre as origen_nombre, o.descripcion as origen_descripcion,
                   a.nombre as alcance_nombre, a.descripcion as alcance_descripcion,
                   est.nombre as estado_actual_nombre, est.ambito as estado_actual_ambito
            FROM eventos_sismicos e
            JOIN clasificaciones_sismo c ON e.clasificacion_id = c.id
            JOIN origenes_generacion o ON e.origen_generacion_id = o.id
            JOIN alcances_sismo a ON e.alcance_sismo_id = a.id
            LEFT JOIN estados est ON e.estado_actual_id = est.id
            WHERE e.id = ?
        ''', (id,))
        
        if not row:
            return None
        
        return self._row_to_entity(row)
    
    def find_all(self) -> List[EventoSismico]:
        rows = self.db.fetch_all('''
            SELECT e.*, c.nombre as clasificacion_nombre, c.km_profundidad_desde, c.km_profundidad_hasta,
                   o.nombre as origen_nombre, o.descripcion as origen_descripcion,
                   a.nombre as alcance_nombre, a.descripcion as alcance_descripcion,
                   est.nombre as estado_actual_nombre, est.ambito as estado_actual_ambito
            FROM eventos_sismicos e
            JOIN clasificaciones_sismo c ON e.clasificacion_id = c.id
            JOIN origenes_generacion o ON e.origen_generacion_id = o.id
            JOIN alcances_sismo a ON e.alcance_sismo_id = a.id
            LEFT JOIN estados est ON e.estado_actual_id = est.id
            ORDER BY e.fecha_hora_concurrencia DESC
        ''')
        
        eventos = []
        for row in rows:
            evento = self._row_to_entity(row)
            if evento:
                eventos.append(evento)
        
        return eventos
    
    def update(self, evento: EventoSismico) -> EventoSismico:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Actualizar clasificación, origen y alcance si es necesario
        clasif_id = self._save_clasificacion(evento.clasificacion)
        origen_id = self._save_origen(evento.origenGeneracion)
        alcance_id = self._save_alcance(evento.alcanceSismo)
        estado_actual_id = self._save_estado(evento.estadoActual)
        
        cursor.execute('''
            UPDATE eventos_sismicos
            SET fecha_hora_concurrencia = ?,
                latitud_epicentro = ?,
                longitud_epicentro = ?,
                latitud_hipocentro = ?,
                longitud_hipocentro = ?,
                valor_magnitud = ?,
                clasificacion_id = ?,
                origen_generacion_id = ?,
                alcance_sismo_id = ?,
                estado_actual_id = ?
            WHERE id = ?
        ''', (
            evento.fechaHoraConcurrencia.isoformat(),
            evento.latitudEpicentro,
            evento.longitudEpicentro,
            evento.latitudHipocentro,
            evento.longitudHipocentro,
            evento.valorMagnitud,
            clasif_id,
            origen_id,
            alcance_id,
            estado_actual_id,
            evento.id
        ))
        
        # Actualizar cambios de estado (eliminar antiguos y guardar nuevos)
        cursor.execute('DELETE FROM cambios_estado WHERE evento_sismico_id = ?', (evento.id,))
        for cambio in evento.cambiosEstado:
            self._save_cambio_estado(cambio, evento.id)
        
        conn.commit()
        return evento
    
    def delete(self, id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Eliminar en cascada (SQLite no tiene CASCADE por defecto, así que lo hacemos manualmente)
        cursor.execute('DELETE FROM detalles_muestra_sismica WHERE muestra_sismica_id IN (SELECT id FROM muestras_sismicas WHERE serie_temporal_id IN (SELECT id FROM series_temporales WHERE evento_sismico_id = ?))', (id,))
        cursor.execute('DELETE FROM muestras_sismicas WHERE serie_temporal_id IN (SELECT id FROM series_temporales WHERE evento_sismico_id = ?)', (id,))
        cursor.execute('DELETE FROM series_temporales WHERE evento_sismico_id = ?', (id,))
        cursor.execute('DELETE FROM cambios_estado WHERE evento_sismico_id = ?', (id,))
        cursor.execute('DELETE FROM eventos_sismicos WHERE id = ?', (id,))
        
        conn.commit()
        return cursor.rowcount > 0
    
    def find_autodetectados(self) -> List[EventoSismico]:
        """Busca eventos que están en estado AutoDetectado o PendienteDeRevision"""
        eventos = self.find_all()
        return [e for e in eventos if e.esAutodetectado()]
    
    def _row_to_entity(self, row) -> Optional[EventoSismico]:
        """Convierte una fila de la BD a una entidad EventoSismico"""
        try:
            clasificacion = ClasificacionSismo(
                row['clasificacion_nombre'],
                row['km_profundidad_desde'],
                row['km_profundidad_hasta']
            )
            origen = OrigenDeGeneracion(
                row['origen_nombre'],
                row['origen_descripcion'] or ''
            )
            alcance = AlcanceSismo(
                row['alcance_nombre'],
                row['alcance_descripcion'] or ''
            )
            
            # Cargar estado actual
            estado_actual = None
            if row['estado_actual_nombre']:
                estado_actual = Estado.getEstadoPorNombre(row['estado_actual_nombre'])
                if not estado_actual:
                    estado_actual = self._create_estado_from_db(row['estado_actual_nombre'], row['estado_actual_ambito'])
            
            # Si no hay estado actual, usar el primer estado disponible (por defecto)
            if not estado_actual:
                estado_actual = PendienteRevision()
            
            evento = EventoSismico(
                row['id'],
                datetime.fromisoformat(row['fecha_hora_concurrencia']),
                row['latitud_epicentro'],
                row['longitud_epicentro'],
                row['latitud_hipocentro'],
                row['longitud_hipocentro'],
                row['valor_magnitud'],
                clasificacion,
                origen,
                alcance,
                estado_actual
            )
            
            # Cargar cambios de estado
            evento.cambiosEstado = self._load_cambios_estado(evento.id)
            
            # Cargar series temporales
            evento.seriesTemporales = self._load_series_temporales(evento.id)
            
            return evento
        except Exception as e:
            print(f"Error al convertir fila a entidad: {e}")
            return None
    
    def _load_cambios_estado(self, evento_id: int) -> List[CambioEstado]:
        """Carga los cambios de estado de un evento"""
        rows = self.db.fetch_all('''
            SELECT ce.*, e.nombre as estado_nombre, e.ambito as estado_ambito
            FROM cambios_estado ce
            JOIN estados e ON ce.estado_id = e.id
            WHERE ce.evento_sismico_id = ?
            ORDER BY ce.fecha_hora_inicio
        ''', (evento_id,))
        
        cambios = []
        for row in rows:
            estado = Estado.getEstadoPorNombre(row['estado_nombre'])
            if not estado:
                # Si el estado no existe en memoria, intentar crearlo desde la BD
                estado = self._create_estado_from_db(row['estado_nombre'], row['estado_ambito'])
            
            if estado:
                cambio = CambioEstado(
                    datetime.fromisoformat(row['fecha_hora_inicio']),
                    estado,
                    row['responsable']
                )
                if row['fecha_hora_fin']:
                    cambio.setFechaHoraFin(datetime.fromisoformat(row['fecha_hora_fin']))
                cambios.append(cambio)
        
        return cambios
    
    def _create_estado_from_db(self, nombre: str, ambito: str) -> Optional[Estado]:
        """Crea un estado desde la BD si no existe en memoria"""
        # Mapeo de nombres a clases de estado
        estado_map = {
            "AutoDetectado": AutoDetectado,
            "Confirmado": Confirmado,
            "Rechazado": Rechazado,
            "DerivadoAExperto": DerivadoAExperto,
            "BloqueadoEnRevision": BloqueadoEnRevision,
            "PendienteRevision": PendienteRevision
        }
        
        estado_class = estado_map.get(nombre)
        if estado_class:
            # Crear instancia (se agregará automáticamente a Estado.estados)
            return estado_class()
        
        return None
    
    def _load_series_temporales(self, evento_id: int) -> List[SerieTemporal]:
        """Carga las series temporales de un evento"""
        rows = self.db.fetch_all('''
            SELECT st.*, s.*, es.*
            FROM series_temporales st
            JOIN sismografos s ON st.sismografo_id = s.id
            JOIN estaciones_sismologicas es ON s.estacion_sismologica_id = es.id
            WHERE st.evento_sismico_id = ?
        ''', (evento_id,))
        
        series = []
        for row in rows:
            estacion = EstacionSismologica(
                row['codigo_estacion'],
                row['documento_certificacion_adq'] or '',
                row['fecha_solicitud_certificacion'] or '',
                row['latitud'],
                row['longitud'],
                row['nombre'],
                row['nro_certificacion_adquisicion'] or ''
            )
            sismografo = Sismografo(
                row['fecha_adquisicion'],
                row['identificador_sismografo'],
                row['nro_serie'] or '',
                estacion
            )
            serie = SerieTemporal(
                datetime.fromisoformat(row['fecha_hora_inicio']),
                row['frecuencia_muestreo'],
                bool(row['condicion_alarma']),
                sismografo
            )
            # Guardar ID de la BD para referencias (usando atributo temporal)
            serie_id_bd = row['id']
            
            # Cargar muestras
            serie.muestrasSismicas = self._load_muestras(serie_id_bd)
            series.append(serie)
        
        return series
    
    def _load_muestras(self, serie_id: int) -> List[MuestraSismica]:
        """Carga las muestras de una serie temporal"""
        rows = self.db.fetch_all('''
            SELECT ms.*, dms.valor, dms.tipo_dato_denominacion, 
                   dms.tipo_dato_unidad_medida, dms.tipo_dato_valor_umbral
            FROM muestras_sismicas ms
            LEFT JOIN detalles_muestra_sismica dms ON ms.id = dms.muestra_sismica_id
            WHERE ms.serie_temporal_id = ?
            ORDER BY ms.fecha_hora_muestra
        ''', (serie_id,))
        
        muestras_dict = {}
        for row in rows:
            muestra_id = row['id']
            if muestra_id not in muestras_dict:
                muestra = MuestraSismica(datetime.fromisoformat(row['fecha_hora_muestra']))
                muestras_dict[muestra_id] = muestra
            
            if row['valor'] is not None:
                tipo_dato = TipoDeDato(
                    row['tipo_dato_denominacion'],
                    row['tipo_dato_unidad_medida'] or '',
                    row['tipo_dato_valor_umbral'] or 0.0
                )
                detalle = DetalleMuestraSismica(row['valor'], tipo_dato)
                muestras_dict[muestra_id].detalleMuestraSismica.append(detalle)
        
        return list(muestras_dict.values())
    
    def _save_clasificacion(self, clasificacion: ClasificacionSismo) -> int:
        """Guarda una clasificación y retorna su ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO clasificaciones_sismo (nombre, km_profundidad_desde, km_profundidad_hasta)
            VALUES (?, ?, ?)
        ''', (clasificacion.nombre, clasificacion.kmProfundidadDesde, clasificacion.kmProfundidadHasta))
        
        if cursor.rowcount == 0:
            # Ya existe, obtener el ID
            row = self.db.fetch_one('SELECT id FROM clasificaciones_sismo WHERE nombre = ?', (clasificacion.nombre,))
            return row['id']
        
        self.db.get_connection().commit()
        return cursor.lastrowid
    
    def _save_origen(self, origen: OrigenDeGeneracion) -> int:
        """Guarda un origen y retorna su ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO origenes_generacion (nombre, descripcion)
            VALUES (?, ?)
        ''', (origen.nombre, origen.descripcion))
        
        if cursor.rowcount == 0:
            row = self.db.fetch_one('SELECT id FROM origenes_generacion WHERE nombre = ?', (origen.nombre,))
            return row['id']
        
        self.db.get_connection().commit()
        return cursor.lastrowid
    
    def _save_alcance(self, alcance: AlcanceSismo) -> int:
        """Guarda un alcance y retorna su ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO alcances_sismo (nombre, descripcion)
            VALUES (?, ?)
        ''', (alcance.nombre, alcance.descripcion))
        
        if cursor.rowcount == 0:
            row = self.db.fetch_one('SELECT id FROM alcances_sismo WHERE nombre = ?', (alcance.nombre,))
            return row['id']
        
        self.db.get_connection().commit()
        return cursor.lastrowid
    
    def _save_cambio_estado(self, cambio: CambioEstado, evento_id: int):
        """Guarda un cambio de estado"""
        # Primero asegurar que el estado existe
        estado_id = self._save_estado(cambio.estado)
        
        # Convertir responsable a string (puede ser Empleado o string)
        responsable_str = cambio.responsable
        if hasattr(cambio.responsable, 'obtenerMail'):
            responsable_str = cambio.responsable.obtenerMail()
        elif hasattr(cambio.responsable, 'getNombre'):
            responsable_str = cambio.responsable.getNombre()
        else:
            responsable_str = str(cambio.responsable)
        
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT INTO cambios_estado 
            (evento_sismico_id, fecha_hora_inicio, fecha_hora_fin, estado_id, responsable)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            evento_id,
            cambio.fechaHoraInicio.isoformat(),
            cambio.fechaHoraFin.isoformat() if cambio.fechaHoraFin else None,
            estado_id,
            responsable_str
        ))
        self.db.get_connection().commit()
    
    def _save_estado(self, estado: Estado) -> int:
        """Guarda un estado y retorna su ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO estados (nombre, ambito)
            VALUES (?, ?)
        ''', (estado.nombreEstado, estado.ambito))
        
        if cursor.rowcount == 0:
            row = self.db.fetch_one('SELECT id FROM estados WHERE nombre = ?', (estado.nombreEstado,))
            return row['id']
        
        self.db.get_connection().commit()
        return cursor.lastrowid
    
    def _save_serie_temporal(self, serie: SerieTemporal, evento_id: int):
        """Guarda una serie temporal y sus muestras"""
        # Primero guardar estación y sismógrafo si no existen
        estacion_id = self._save_estacion(serie.sismografo.estacionSismologica)
        sismografo_id = self._save_sismografo(serie.sismografo, estacion_id)
        
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT INTO series_temporales
            (evento_sismico_id, fecha_hora_inicio, frecuencia_muestreo, condicion_alarma, sismografo_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            evento_id,
            serie.fechaHoraInicio.isoformat(),
            serie.frecuenciaMuestreo,
            1 if serie.condicionAlarma else 0,
            sismografo_id
        ))
        
        serie_id = cursor.lastrowid
        
        # Guardar muestras
        for muestra in serie.muestrasSismicas:
            self._save_muestra(muestra, serie_id)
        
        self.db.get_connection().commit()
    
    def _save_estacion(self, estacion: EstacionSismologica) -> int:
        """Guarda una estación y retorna su ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO estaciones_sismologicas
            (codigo_estacion, documento_certificacion_adq, fecha_solicitud_certificacion,
             latitud, longitud, nombre, nro_certificacion_adquisicion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            estacion.codigoEstacion,
            estacion.documentoCertificacionAdq,
            estacion.fechaSolicitudCertificacion,
            estacion.latitud,
            estacion.longitud,
            estacion.nombre,
            estacion.nroCertificacionAdquisicion
        ))
        
        if cursor.rowcount == 0:
            row = self.db.fetch_one('SELECT id FROM estaciones_sismologicas WHERE codigo_estacion = ?', 
                                   (estacion.codigoEstacion,))
            return row['id']
        
        self.db.get_connection().commit()
        return cursor.lastrowid
    
    def _save_sismografo(self, sismografo: Sismografo, estacion_id: int) -> int:
        """Guarda un sismógrafo y retorna su ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO sismografos
            (fecha_adquisicion, identificador_sismografo, nro_serie, estacion_sismologica_id)
            VALUES (?, ?, ?, ?)
        ''', (
            sismografo.fechaAdquisicion,
            sismografo.identificadorSismografo,
            sismografo.nroSerie,
            estacion_id
        ))
        
        if cursor.rowcount == 0:
            row = self.db.fetch_one('SELECT id FROM sismografos WHERE identificador_sismografo = ?',
                                   (sismografo.identificadorSismografo,))
            return row['id']
        
        self.db.get_connection().commit()
        return cursor.lastrowid
    
    def _save_muestra(self, muestra: MuestraSismica, serie_id: int):
        """Guarda una muestra y sus detalles"""
        cursor = self.db.get_connection().cursor()
        cursor.execute('''
            INSERT INTO muestras_sismicas (serie_temporal_id, fecha_hora_muestra)
            VALUES (?, ?)
        ''', (serie_id, muestra.fechaHoraMuestra.isoformat()))
        
        muestra_id = cursor.lastrowid
        
        # Guardar detalles
        for detalle in muestra.detalleMuestraSismica:
            cursor.execute('''
                INSERT INTO detalles_muestra_sismica
                (muestra_sismica_id, valor, tipo_dato_denominacion, tipo_dato_unidad_medida, tipo_dato_valor_umbral)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                muestra_id,
                detalle.valor,
                detalle.tipoDeDato.denominacion,
                detalle.tipoDeDato.nombreUnidadMedida,
                detalle.tipoDeDato.valorUmbral
            ))
        
        self.db.get_connection().commit()

