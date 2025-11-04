class EstacionSismologica:
    def __init__(self, codigoEstacion: str, documentoCertificacionAdq: str, fechaSolicitudCertificacion: str, latitud: float, longitud: float, nombre: str, nroCertificacionAdquisicion: str):
        self.codigoEstacion = codigoEstacion
        self.documentoCertificacionAdq = documentoCertificacionAdq
        self.fechaSolicitudCertificacion = fechaSolicitudCertificacion
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.nroCertificacionAdquisicion = nroCertificacionAdquisicion

    def getCodigoEstacion(self) -> str:
        return self.codigoEstacion

    def getNombre(self) -> str:
        return self.nombre