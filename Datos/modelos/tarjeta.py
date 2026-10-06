class Tarjeta:
    def __init__(self, id_tarjeta, id_lista, titulo, descripcion, fecha_limite, estado):
        self.__id_tarjeta = id_tarjeta
        self.__id_lista = id_lista
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__fecha_limite = fecha_limite
        self.__estado = estado