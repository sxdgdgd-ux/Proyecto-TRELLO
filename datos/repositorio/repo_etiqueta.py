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


def obtener_etiqueta_por_id(id_etiqueta):
    """Busca una etiqueta por ID."""
    return Etiqueta.get_or_none(Etiqueta.id_etiqueta == id_etiqueta)


def actualizar_etiqueta(id_etiqueta, nombre=None, color=None):
    """Actualiza los campos indicados de una etiqueta."""
    etiqueta = obtener_etiqueta_por_id(id_etiqueta)
    if not etiqueta:
        return None
    if nombre is not None:
        etiqueta.nombre = nombre
    if color is not None:
        etiqueta.color = color
    etiqueta.save()
    return etiqueta


def asignar_etiqueta_a_tarjeta(id_tarjeta, id_etiqueta):
    """Asigna una etiqueta a una tarjeta específica."""
    return TarjetaEtiqueta.create(id_tarjeta=id_tarjeta, id_etiqueta=id_etiqueta)


def eliminar_etiqueta_de_tarjeta(id_tarjeta, id_etiqueta):
    """Retira una etiqueta de una tarjeta."""
    return (
        TarjetaEtiqueta.delete()
        .where(
            (TarjetaEtiqueta.id_tarjeta == id_tarjeta)
            & (TarjetaEtiqueta.id_etiqueta == id_etiqueta)
        )
        .execute()
        > 0
    )


def eliminar_etiqueta(id_etiqueta):
    """Elimina físicamente una etiqueta por ID."""
    etiqueta = obtener_etiqueta_por_id(id_etiqueta)
    if not etiqueta:
        return False
    etiqueta.delete_instance()
    return True