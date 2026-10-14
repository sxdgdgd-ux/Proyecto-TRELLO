"""Módulo de repositorio para la gestión de Comentarios."""
from Datos.modelos.models import Comentario


def crear_comentario(id_tarjeta, id_usuario, texto):
    """Registra un nuevo comentario en una tarjeta."""
    return Comentario.create(id_tarjeta=id_tarjeta, id_usuario=id_usuario, texto=texto)


def listado_comentarios_por_tarjeta(id_tarjeta):
    """Lista los comentarios de una tarjeta concreta."""
    comentarios = Comentario.select().where(Comentario.id_tarjeta == id_tarjeta)
    if not comentarios:
        print("No hay comentarios en esta tarjeta.")
    return comentarios


def eliminar_comentario(id_comentario):
    """Elimina un comentario por su ID."""
    comentario = Comentario.get_or_none(Comentario.id_comentario == id_comentario)
    if comentario:
        comentario.delete_instance()
        return True
    return False