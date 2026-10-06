from datos.modelos.entidades.entidad_Tarjeta import Tarjeta, AsignacionTarjeta

def crear_tarjeta(id_lista, titulo, descripcion=None, fecha_limite=None, estado=None):
    return Tarjeta.create(
        id_lista=id_lista,
        titulo=titulo,
        descripcion=descripcion,
        fecha_limite=fecha_limite,
        estado=estado
    )

def listado_tarjetas_por_lista(id_lista):
    tarjetas = Tarjeta.select().where(Tarjeta.id_lista == id_lista)
    if not tarjetas:
        print("No hay tarjetas en esta lista.")
    return tarjetas

def obtener_tarjeta_por_id(id_tarjeta):
    return Tarjeta.get_or_none(Tarjeta.id_tarjeta == id_tarjeta)

def asignar_usuario_a_tarjeta(id_tarjeta, id_usuario):
    return AsignacionTarjeta.create(id_tarjeta=id_tarjeta, id_usuario=id_usuario)

def eliminar_tarjeta(id_tarjeta):
    tarjeta = obtener_tarjeta_por_id(id_tarjeta)
    if tarjeta:
        tarjeta.delete_instance()
        return True
    return False