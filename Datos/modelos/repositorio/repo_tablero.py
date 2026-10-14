"""Módulo de repositorio para la gestión de Tableros."""
from Datos.modelos.models import Tablero


def crear_tablero(id_proyecto, titulo):
    """Crea un nuevo tablero dentro de un proyecto."""
    return Tablero.create(id_proyecto=id_proyecto, titulo=titulo)


def listado_tableros_por_proyecto(id_proyecto):
    """Lista todos los tableros pertenecientes a un proyecto."""
    tableros = Tablero.select().where(Tablero.id_proyecto == id_proyecto)
    if not tableros:
        print("No hay tableros en este proyecto.")
    return tableros


def obtener_tablero_por_id(id_tablero):
    """Obtiene un tablero específico por ID."""
    return Tablero.get_or_none(Tablero.id_tablero == id_tablero)


def eliminar_tablero(id_tablero):
    """Elimina un tablero."""
    tablero = obtener_tablero_por_id(id_tablero)
    if tablero:
        tablero.delete_instance()
        return True
    return False