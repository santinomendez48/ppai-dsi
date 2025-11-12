import sqlite3
import os
from typing import Optional

class Database:
    _instance: Optional['Database'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._connection is None:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sismologia.db')
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._create_tables()
    
    def get_connection(self) -> sqlite3.Connection:
        return self._connection
    
    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def _create_tables(self):
        cursor = self._connection.cursor()
        
        # Tabla de estados (valores de referencia)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                ambito TEXT NOT NULL
            )
        ''')
        
        # Tabla de clasificaciones de sismo (valores de referencia)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clasificaciones_sismo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                km_profundidad_desde REAL NOT NULL,
                km_profundidad_hasta REAL NOT NULL
            )
        ''')
        
        # Tabla de orígenes de generación (valores de referencia)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS origenes_generacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT
            )
        ''')
        
        # Tabla de alcances de sismo (valores de referencia)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alcances_sismo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT
            )
        ''')
        
        # Tabla de estaciones sismológicas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estaciones_sismologicas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_estacion TEXT UNIQUE NOT NULL,
                documento_certificacion_adq TEXT,
                fecha_solicitud_certificacion TEXT,
                latitud REAL NOT NULL,
                longitud REAL NOT NULL,
                nombre TEXT NOT NULL,
                nro_certificacion_adquisicion TEXT
            )
        ''')
        
        # Tabla de sismógrafos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sismografos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_adquisicion TEXT NOT NULL,
                identificador_sismografo TEXT UNIQUE NOT NULL,
                nro_serie TEXT,
                estacion_sismologica_id INTEGER NOT NULL,
                FOREIGN KEY (estacion_sismologica_id) REFERENCES estaciones_sismologicas(id)
            )
        ''')
        
        # Tabla de eventos sísmicos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos_sismicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_hora_concurrencia TEXT NOT NULL,
                latitud_epicentro REAL NOT NULL,
                longitud_epicentro REAL NOT NULL,
                latitud_hipocentro REAL NOT NULL,
                longitud_hipocentro REAL NOT NULL,
                valor_magnitud REAL NOT NULL,
                clasificacion_id INTEGER NOT NULL,
                origen_generacion_id INTEGER NOT NULL,
                alcance_sismo_id INTEGER NOT NULL,
                estado_actual_id INTEGER,
                FOREIGN KEY (clasificacion_id) REFERENCES clasificaciones_sismo(id),
                FOREIGN KEY (origen_generacion_id) REFERENCES origenes_generacion(id),
                FOREIGN KEY (alcance_sismo_id) REFERENCES alcances_sismo(id),
                FOREIGN KEY (estado_actual_id) REFERENCES estados(id)
            )
        ''')
        
        # Tabla de cambios de estado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cambios_estado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evento_sismico_id INTEGER NOT NULL,
                fecha_hora_inicio TEXT NOT NULL,
                fecha_hora_fin TEXT,
                estado_id INTEGER NOT NULL,
                responsable TEXT NOT NULL,
                FOREIGN KEY (evento_sismico_id) REFERENCES eventos_sismicos(id),
                FOREIGN KEY (estado_id) REFERENCES estados(id)
            )
        ''')
        
        # Tabla de series temporales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS series_temporales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evento_sismico_id INTEGER NOT NULL,
                fecha_hora_inicio TEXT NOT NULL,
                frecuencia_muestreo REAL NOT NULL,
                condicion_alarma INTEGER NOT NULL,
                sismografo_id INTEGER NOT NULL,
                FOREIGN KEY (evento_sismico_id) REFERENCES eventos_sismicos(id),
                FOREIGN KEY (sismografo_id) REFERENCES sismografos(id)
            )
        ''')
        
        # Tabla de muestras sísmicas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS muestras_sismicas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serie_temporal_id INTEGER NOT NULL,
                fecha_hora_muestra TEXT NOT NULL,
                FOREIGN KEY (serie_temporal_id) REFERENCES series_temporales(id)
            )
        ''')
        
        # Tabla de detalles de muestra sísmica
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalles_muestra_sismica (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                muestra_sismica_id INTEGER NOT NULL,
                valor REAL NOT NULL,
                tipo_dato_denominacion TEXT NOT NULL,
                tipo_dato_unidad_medida TEXT,
                tipo_dato_valor_umbral REAL,
                FOREIGN KEY (muestra_sismica_id) REFERENCES muestras_sismicas(id)
            )
        ''')
        
        self._connection.commit()
    
    def execute_query(self, query: str, params: tuple = ()):
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        self._connection.commit()
        return cursor
    
    def fetch_all(self, query: str, params: tuple = ()):
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query: str, params: tuple = ()):
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

