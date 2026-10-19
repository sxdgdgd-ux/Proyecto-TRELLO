"""Módulo de repositorio para la gestión de Etiquetas."""
from Datos.modelos.models import Etiqueta, TarjetaEtiqueta


def crear_etiqueta(nombre, color):
    """Crea una etiqueta nueva."""
    return Etiqueta.create(nombre=nombre, color=color)


def listado_etiquetas():
    """Obtiene el listado de todas las etiquetas."""
    etiquetas = Etiqueta.select().order_by(Etiqueta.nombre)
    if not etiquetas:
        print("No hay etiquetas registradas.")
    return etiquetas


def asignar_etiqueta_a_tarjeta(id_tarjeta, id_etiqueta):
    """Asigna una etiqueta a una tarjeta específica."""
    return TarjetaEtiqueta.create(id_tarjeta=id_tarjeta, id_etiqueta=id_etiqueta)