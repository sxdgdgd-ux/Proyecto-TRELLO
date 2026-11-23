"""Módulo de repositorio para la gestión de Proyectos."""
from Datos.modelos.models import Proyecto, ProyectoUsuario

ROLES = ("Administrador", "Lider", "Miembro", "Observador")
SIN_CAMBIO = object()


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


def actualizar_proyecto(
    id_proyecto, nombre_proyecto=None, descripcion=SIN_CAMBIO
):
    """Actualiza los campos indicados de un proyecto."""
    proyecto = obtener_proyecto_por_id(id_proyecto)
    if not proyecto:
        return None
    if nombre_proyecto is not None:
        proyecto.nombre_proyecto = nombre_proyecto
    if descripcion is not SIN_CAMBIO:
        proyecto.descripcion = descripcion
    proyecto.save()
    return proyecto


def asignar_usuario_a_proyecto(id_proyecto, id_usuario, rol):
    """Asigna un usuario a un proyecto con un rol determinado."""
    if rol not in ROLES:
        raise ValueError(f"Rol inválido. Valores permitidos: {', '.join(ROLES)}.")
    asignacion, _ = ProyectoUsuario.get_or_create(
        id_proyecto=id_proyecto,
        id_usuario=id_usuario,
        defaults={"rol": rol},
    )
    if asignacion.rol != rol:
        asignacion.rol = rol
        asignacion.save()
    return asignacion


def obtener_rol_usuario(id_proyecto, id_usuario):
    """Devuelve el rol del usuario en el proyecto o None si no está asignado."""
    asignacion = ProyectoUsuario.get_or_none(
        (ProyectoUsuario.id_proyecto == id_proyecto)
        & (ProyectoUsuario.id_usuario == id_usuario)
    )
    return asignacion.rol if asignacion else None


def listar_usuarios_proyecto(id_proyecto):
    """Lista las asignaciones de miembros de un proyecto."""
    return (
        ProyectoUsuario.select()
        .where(ProyectoUsuario.id_proyecto == id_proyecto)
        .order_by(ProyectoUsuario.id_usuario)
    )


def eliminar_usuario_de_proyecto(id_proyecto, id_usuario):
    """Quita la asignación de un usuario al proyecto."""
    return (
        ProyectoUsuario.delete()
        .where(
            (ProyectoUsuario.id_proyecto == id_proyecto)
            & (ProyectoUsuario.id_usuario == id_usuario)
        )
        .execute()
        > 0
    )


def eliminar_proyecto(id_proyecto):
    """Elimina un proyecto existente."""
    proyecto = obtener_proyecto_por_id(id_proyecto)
    if proyecto:
        proyecto.delete_instance()
        return True
    return False
