"""Módulo de repositorio para la gestión de Usuarios."""
from datos.modelos.models import Usuario


def guardar(usuario):
    """Persiste un usuario y devuelve la instancia guardada."""
    usuario.save()
    return usuario


def crear_usuario(nombre, email, password_hash, es_admin=False):
    """Crea un usuario nuevo."""
    usuario = Usuario(
        nombre=nombre,
        email=email,
        password_hash=password_hash,
        es_admin=es_admin,
    )
    return guardar(usuario)


def listado_usuarios():
    """Obtiene el listado de todos los usuarios registrados."""
    return list(Usuario.select().order_by(Usuario.nombre, Usuario.id_usuario))


def obtener_usuario_por_id(id_usuario):
    """Busca y retorna un usuario por su ID."""
    return Usuario.get_or_none(Usuario.id_usuario == id_usuario)


def obtener_usuario_por_email(email):
    """Busca y retorna un usuario por su correo."""
    return Usuario.get_or_none(Usuario.email == email)


def actualizar_usuario(
    id_usuario, nombre=None, email=None, password_hash=None, es_admin=None
):
    """Actualiza los datos de un usuario existente."""
    usuario = obtener_usuario_por_id(id_usuario)
    if usuario:
        if nombre is not None:
            usuario.nombre = nombre
        if email is not None:
            usuario.email = email
        if password_hash is not None:
            usuario.password_hash = password_hash
        if es_admin is not None:
            usuario.es_admin = es_admin
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
