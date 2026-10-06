from datos.modelos.entidades.entidad_Tablero import Tablero

def crear_tablero(id_proyecto, titulo):
    return Tablero.create(id_proyecto=id_proyecto, titulo=titulo)

def listado_tableros_por_proyecto(id_proyecto):
    tableros = Tablero.select().where(Tablero.id_proyecto == id_proyecto)
    if not tableros:
        print("No hay tableros en este proyecto.")
    return tableros

def obtener_tablero_por_id(id_tablero):
    return Tablero.get_or_none(Tablero.id_tablero == id_tablero)

def eliminar_tablero(id_tablero):
    tablero = obtener_tablero_por_id(id_tablero)
    if tablero:
        tablero.delete_instance()
        return True
    return False