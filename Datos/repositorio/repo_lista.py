"""Módulo de repositorio para la gestión de Listas."""
from Datos.modelos.models import Lista


def crear_lista(id_tablero, nombre_lista, posicion):
    """Crea una nueva lista dentro de un tablero."""
    return Lista.create(id_tablero=id_tablero, nombre_lista=nombre_lista, posicion=posicion)


def listado_listas_por_tablero(id_tablero):
    """Obtiene las listas de un tablero ordenadas por posición."""
    listas = Lista.select().where(Lista.id_tablero == id_tablero).order_by(Lista.posicion)
    if not listas:
        print("No hay listas en este tablero.")
    return listas


def obtener_lista_por_id(id_lista):
    """Busca una lista por su ID."""
    return Lista.get_or_none(Lista.id_lista == id_lista)


def actualizar_lista(id_lista, nombre_lista=None, posicion=None, id_tablero=None):
    """Actualiza los campos indicados de una lista."""
    lista = obtener_lista_por_id(id_lista)
    if not lista:
        return None
    if nombre_lista is not None:
        lista.nombre_lista = nombre_lista
    if posicion is not None:
        lista.posicion = posicion
    if id_tablero is not None:
        lista.id_tablero = id_tablero
    lista.save()
    return lista


def eliminar_lista(id_lista):
    """Elimina una lista de tareas."""
    lista = obtener_lista_por_id(id_lista)
    if lista:
        lista.delete_instance()
        return True
    return False
