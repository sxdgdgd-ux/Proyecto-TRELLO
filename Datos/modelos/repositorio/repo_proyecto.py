"""Módulo de repositorio para la gestión de Proyectos."""
from Datos.modelos.models import Proyecto, ProyectoUsuario


def crear_proyecto(nombre_proyecto, descripcion=None):
    """Crea un nuevo proyecto."""
    return Proyecto.create(nombre_proyecto=nombre_proyecto, descripcion=descripcion)


def listado_proyectos():
    """Obtiene el listado de todos los proyectos."""
    proyectos = Proyecto.select()
    if not proyectos:
        print("No hay proyectos registrados.")
    return proyectos


def obtener_proyecto_por_id(id_proyecto):
    """Busca un proyecto por su ID."""
    return Proyecto.get_or_none(Proyecto.id_proyecto == id_proyecto)


def asignar_usuario_a_proyecto(id_proyecto, id_usuario, rol):
    """Asigna un usuario a un proyecto con un rol determinado."""
    return ProyectoUsuario.create(id_proyecto=id_proyecto, id_usuario=id_usuario, rol=rol)


def eliminar_proyecto(id_proyecto):
    """Elimina un proyecto existente."""
    proyecto = obtener_proyecto_por_id(id_proyecto)
    if proyecto:
        proyecto.delete_instance()
        return True
    return False
