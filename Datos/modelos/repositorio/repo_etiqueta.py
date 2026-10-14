from Datos.modelos.etiqueta import Etiqueta, TarjetaEtiqueta

def crear_etiqueta(nombre, color):
    return Etiqueta.create(nombre=nombre, color=color)  # pylint: disable=no-member

def listado_etiquetas():
    etiquetas = Etiqueta.select()  # pylint: disable=no-member
    if not etiquetas:
        print("No hay etiquetas registradas.")
    return etiquetas

def asignar_etiqueta_a_tarjeta(id_tarjeta, id_etiqueta):
    return TarjetaEtiqueta.create(id_tarjeta=id_tarjeta, id_etiqueta=id_etiqueta)