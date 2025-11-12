import random
from datetime import datetime, timedelta
from entities.evento_sismico import EventoSismico
from entities.clasificacion_sismo import ClasificacionSismo
from entities.origen_de_generacion import OrigenDeGeneracion
from entities.alcance_sismo import AlcanceSismo
from entities.cambio_estado import CambioEstado
from entities.estados_concretos.estado_pendiente_revision import PendienteRevision
from entities.estacion_sismologica import EstacionSismologica
from entities.sismografo import Sismografo
from entities.serie_temporal import SerieTemporal
from entities.muestra_sismica import MuestraSismica
from entities.tipo_de_dato import TipoDeDato
from persistence.repositories.evento_sismico_repository import EventoSismicoRepository

def generar_eventos_sismicos():
    """
    Genera 5 eventos sísmicos con datos aleatorios
    Estado inicial: Pendiente de Revisión
    Incluye series temporales, sismógrafos, estaciones, muestras y detalles
    """
    
    # Crear instancia del repositorio
    repo = EventoSismicoRepository()
    
    # Definir datos de referencia
    clasificaciones = [
        ClasificacionSismo("Superficial", 0, 70),
        ClasificacionSismo("Intermedio", 70, 300),
        ClasificacionSismo("Profundo", 300, 700),
    ]
    
    origenes = [
        OrigenDeGeneracion("Tectónico", "Causado por movimiento tectónico"),
        OrigenDeGeneracion("Volcánico", "Asociado a actividad volcánica"),
        OrigenDeGeneracion("Inducido", "Causado por actividad humana"),
    ]
    
    alcances = [
        AlcanceSismo("Local", "Sentido a menos de 100 km"),
        AlcanceSismo("Regional", "Sentido entre 100 y 1000 km"),
        AlcanceSismo("Teleseísmo", "Sentido a más de 1000 km"),
    ]
    
    # Tipos de datos para muestras
    tipos_datos = [
        TipoDeDato("Longitud de Onda", "metros", 100.0),
        TipoDeDato("Frecuencia de Onda", "Hz", 50.0),
        TipoDeDato("Velocidad de Onda", "m/s", 1000.0),
    ]
    
    # Nombres de estaciones
    nombres_estaciones = [
        "Estación Sísmica Central",
        "Estación Sísmica Norte",
        "Estación Sísmica Sur",
        "Estación Sísmica Este",
        "Estación Sísmica Oeste",
    ]
    
    # Crear estado "Pendiente de Revisión"
    estado_pendiente = PendienteRevision()
    
    # Generar 5 eventos sísmicos
    eventos = []
    fecha_base = datetime.now() - timedelta(days=30)
    
    for i in range(5):
        # Generar datos aleatorios del evento
        fecha_evento = fecha_base + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        
        latitud_epicentro = round(random.uniform(-90, 90), 4)
        longitud_epicentro = round(random.uniform(-180, 180), 4)
        latitud_hipocentro = round(random.uniform(-90, 90), 4)
        longitud_hipocentro = round(random.uniform(-180, 180), 4)
        
        magnitud = round(random.uniform(3.0, 8.0), 1)
        
        clasificacion = random.choice(clasificaciones)
        origen = random.choice(origenes)
        alcance = random.choice(alcances)
        
        # Crear evento sísmico
        evento = EventoSismico(
            id=0,  # Se asignará automáticamente en la BD
            fechaHoraConcurrencia=fecha_evento,
            latitudEpicentro=latitud_epicentro,
            longitudEpicentro=longitud_epicentro,
            latitudHipocentro=latitud_hipocentro,
            longitudHipocentro=longitud_hipocentro,
            valorMagnitud=magnitud,
            clasificacion=clasificacion,
            origenGeneracion=origen,
            alcanceSismo=alcance,
            estadoActual=estado_pendiente
        )
        
        # Crear cambio de estado inicial (Pendiente de Revisión)
        cambio_inicial = CambioEstado(
            fechaHoraInicio=fecha_evento,
            estado=estado_pendiente,
            responsable="SISTEMA"
        )
        evento.agregarCambioEstado(cambio_inicial)
        
        # Generar al menos 2 series temporales por evento (2-4)
        num_series = random.randint(2, 4)
        for j in range(num_series):
            # Crear estación sismológica aleatoria
            nombre_estacion = random.choice(nombres_estaciones)
            codigo_estacion = f"EST-{i+1}-{j+1}"
            
            estacion = EstacionSismologica(
                codigoEstacion=codigo_estacion,
                documentoCertificacionAdq=f"DOC-{i+1}-{j+1}",
                fechaSolicitudCertificacion=(fecha_evento - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                latitud=round(random.uniform(-90, 90), 4),
                longitud=round(random.uniform(-180, 180), 4),
                nombre=nombre_estacion,
                nroCertificacionAdquisicion=f"CERT-{i+1}-{j+1}"
            )
            
            # Crear sismógrafo
            sismografo = Sismografo(
                fechaAquisicion=(fecha_evento - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d'),
                identificadorSismografo=f"SISMORAFO-{i+1}-{j+1}",
                nroSerie=f"SN-{i+1}-{j+1}-{random.randint(1000, 9999)}",
                estacionSismologica=estacion
            )
            
            # Crear serie temporal
            serie = SerieTemporal(
                fechaHoraInicio=fecha_evento + timedelta(minutes=random.randint(0, 60)),
                frecuenciaMuestreo=round(random.uniform(10.0, 100.0), 2),
                condicionAlarma=random.choice([True, False]),
                sismografo=sismografo
            )
            
            # Generar muestras sísmicas (10-20 muestras por serie)
            num_muestras = random.randint(10, 20)
            for k in range(num_muestras):
                fecha_muestra = fecha_evento + timedelta(minutes=k*5, seconds=random.randint(0, 59))
                muestra = MuestraSismica(fechaHoraMuestra=fecha_muestra)
                
                # Agregar 1-3 detalles por muestra
                num_detalles = random.randint(1, 3)
                tipos_seleccionados = random.sample(tipos_datos, min(num_detalles, len(tipos_datos)))
                
                for tipo_dato in tipos_seleccionados:
                    valor = round(random.uniform(tipo_dato.valorUmbral * 0.5, tipo_dato.valorUmbral * 2), 2)
                    muestra.crearDetalleMuestra(valor, tipo_dato)
                
                serie.muestrasSismicas.append(muestra)
            
            evento.seriesTemporales.append(serie)
        
        # Guardar evento en la BD
        evento_guardado = repo.save(evento)
        eventos.append(evento_guardado)
        
        print(f"✓ Evento {i+1} creado:")
        print(f"  ID: {evento_guardado.id}")
        print(f"  Fecha: {evento_guardado.fechaHoraConcurrencia}")
        print(f"  Magnitud: {evento_guardado.valorMagnitud}")
        print(f"  Clasificación: {evento_guardado.clasificacion.nombre}")
        print(f"  Origen: {evento_guardado.origenGeneracion.nombre}")
        print(f"  Alcance: {evento_guardado.alcanceSismo.nombre}")
        print(f"  Estado: {evento_guardado.estadoActual.nombreEstado}")
        print(f"  Series temporales: {len(evento_guardado.seriesTemporales)}")
        
        total_muestras = sum(len(serie.muestrasSismicas) for serie in evento_guardado.seriesTemporales)
        print(f"  Total de muestras sísmicas: {total_muestras}")
        print()
    
    print(f"\n✅ Se han creado {len(eventos)} eventos sísmicos exitosamente")
    
    # Verificar que se guardaron correctamente
    eventos_bd = repo.find_all()
    print(f"Total de eventos en la BD: {len(eventos_bd)}")
    
    # Mostrar detalles de un evento
    if eventos_bd:
        primer_evento = eventos_bd[0]
        print(f"\nDetalles del primer evento (ID: {primer_evento.id}):")
        print(f"  Series temporales: {len(primer_evento.seriesTemporales)}")
        for idx, serie in enumerate(primer_evento.seriesTemporales):
            print(f"    Serie {idx+1}:")
            print(f"      Estación: {serie.getEstacionSismologica().nombre}")
            print(f"      Sismógrafo: {serie.sismografo.identificadorSismografo}")
            print(f"      Frecuencia: {serie.frecuenciaMuestreo} Hz")
            print(f"      Muestras: {len(serie.muestrasSismicas)}")
    
    return eventos

if __name__ == "__main__":
    generar_eventos_sismicos()
