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


def eliminar_lista(id_lista):
    """Elimina una lista de tareas."""
    lista = obtener_lista_por_id(id_lista)
    if lista:
        lista.delete_instance()
        return True
    return False
