from datos.modelos.entidades.entidad_Proyecto import Proyecto, ProyectoUsuario

def crear_proyecto(nombre_proyecto, descripcion=None):
    return Proyecto.create(nombre_proyecto=nombre_proyecto, descripcion=descripcion)

def listado_proyectos():
    proyectos = Proyecto.select()
    if not proyectos:
        print("No hay proyectos registrados.")
    return proyectos

def obtener_proyecto_por_id(id_proyecto):
    return Proyecto.get_or_none(Proyecto.id_proyecto == id_proyecto)

def asignar_usuario_a_proyecto(id_proyecto, id_usuario, rol):
    return ProyectoUsuario.create(id_proyecto=id_proyecto, id_usuario=id_usuario, rol=rol)

def eliminar_proyecto(id_proyecto):
    proyecto = obtener_proyecto_por_id(id_proyecto)
    if proyecto:
        proyecto.delete_instance()
        return True
    return False