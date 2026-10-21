"""Módulo de repositorio para la gestión de Tableros."""
from Datos.modelos.models import Tablero, TableroUsuario

ROLES = ("Administrador", "Lider", "Miembro", "Observador")


def crear_tablero(id_proyecto, titulo):
    """Crea un nuevo tablero dentro de un proyecto."""
    return Tablero.create(id_proyecto=id_proyecto, titulo=titulo)


def listado_tableros_por_proyecto(id_proyecto):
    """Lista todos los tableros pertenecientes a un proyecto."""
    tableros = Tablero.select().where(Tablero.id_proyecto == id_proyecto)
    if not tableros:
        print("No hay tableros en este proyecto.")
    return tableros


def listado_tableros():
    """Lista todos los tableros."""
    return Tablero.select().order_by(Tablero.id_tablero)


def obtener_tablero_por_id(id_tablero):
    """Obtiene un tablero específico por ID."""
    return Tablero.get_or_none(Tablero.id_tablero == id_tablero)


def actualizar_tablero(id_tablero, id_proyecto=None, titulo=None):
    """Actualiza los campos indicados de un tablero."""
    tablero = obtener_tablero_por_id(id_tablero)
    if not tablero:
        return None
    if id_proyecto is not None:
        tablero.id_proyecto = id_proyecto
    if titulo is not None:
        tablero.titulo = titulo
    tablero.save()
    return tablero


def obtener_rol_usuario(id_tablero, id_usuario):
    """Devuelve el rol del usuario en el tablero o None si no está asignado."""
    asignacion = TableroUsuario.get_or_none(
        (TableroUsuario.id_tablero == id_tablero)
        & (TableroUsuario.id_usuario == id_usuario)
    )
    return asignacion.rol if asignacion else None


def listar_usuarios_tablero(id_tablero):
    """Lista las asignaciones de roles de un tablero."""
    return (
        TableroUsuario.select()
        .where(TableroUsuario.id_tablero == id_tablero)
        .order_by(TableroUsuario.id_usuario)
    )


def asignar_usuario_a_tablero(id_tablero, id_usuario, rol):
    """Asigna o actualiza el rol de un usuario en un tablero."""
    if rol not in ROLES:
        raise ValueError(f"Rol inválido. Valores permitidos: {', '.join(ROLES)}.")
    asignacion, _ = TableroUsuario.get_or_create(
        id_tablero=id_tablero,
        id_usuario=id_usuario,
        defaults={"rol": rol},
    )
    if asignacion.rol != rol:
        asignacion.rol = rol
        asignacion.save()
    return asignacion


def eliminar_usuario_de_tablero(id_tablero, id_usuario):
    """Quita la asignación de un usuario al tablero."""
    return (
        TableroUsuario.delete()
        .where(
            (TableroUsuario.id_tablero == id_tablero)
            & (TableroUsuario.id_usuario == id_usuario)
        )
        .execute()
        > 0
    )


def eliminar_tablero(id_tablero):
    """Elimina un tablero."""
    tablero = obtener_tablero_por_id(id_tablero)
    if tablero:
        tablero.delete_instance()
        return True
    return False