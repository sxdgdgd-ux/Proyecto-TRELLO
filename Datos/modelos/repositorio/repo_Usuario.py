from datos.modelos.entidades.entidad_Usuario import Usuario

def listado_usuarios():
    usuarios = Usuario.select()
    if not usuarios:
        print("No hay usuarios registrados.")
    return usuarios