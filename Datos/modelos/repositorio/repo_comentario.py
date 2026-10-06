from datos.modelos.entidades.entidad_Comentario import Comentario

def crear_comentario(id_tarjeta, id_usuario, texto):
    return Comentario.create(id_tarjeta=id_tarjeta, id_usuario=id_usuario, texto=texto)

def listado_comentarios_por_tarjeta(id_tarjeta):
    comentarios = Comentario.select().where(Comentario.id_tarjeta == id_tarjeta)
    if not comentarios:
        print("No hay comentarios en esta tarjeta.")
    return comentarios

def eliminar_comentario(id_comentario):
    comentario = Comentario.get_or_none(Comentario.id_comentario == id_comentario)
    if comentario:
        comentario.delete_instance()
        return True
    return False