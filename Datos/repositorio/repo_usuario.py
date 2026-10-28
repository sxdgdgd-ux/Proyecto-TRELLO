"""Módulo de repositorio para la gestión de Usuarios."""
from Datos.modelos.models import Usuario


def crear_usuario(nombre, email):
    """Crea un nuevo usuario o recupera el existente si el correo ya esta registrado."""
    usuario, creado = Usuario.get_or_create(
        email=email,
        defaults={'nombre': nombre}
    )
    return usuario

def listado_usuarios():
    """Obtiene el listado de todos los usuarios registrados."""
    return list(Usuario.select().order_by(Usuario.nombre, Usuario.id_usuario))


def obtener_usuario_por_id(id_usuario):
    """Busca y retorna un usuario por su ID."""
    return Usuario.get_or_none(Usuario.id_usuario == id_usuario)


def actualizar_usuario(id_usuario, nombre=None, email=None):
    """Actualiza los datos de un usuario existente."""
    usuario = obtener_usuario_por_id(id_usuario)
    if usuario:
        if nombre:
            usuario.nombre = nombre
        if email:
            usuario.email = email
        usuario.save()
        return usuario
    return None


def eliminar_usuario(id_usuario):
    """Elimina un usuario por su ID."""
    usuario = obtener_usuario_por_id(id_usuario)
    if usuario:
        usuario.delete_instance()
        return True
    return False
