"""Módulo de repositorio para la gestión de Etiquetas."""
from Datos.modelos.models import (
    AsignacionTarjeta,
    Etiqueta,
    Tarjeta,
    TarjetaEtiqueta,
)

SIN_CAMBIO = object()


def crear_tarjeta(id_lista, titulo, descripcion=None, fecha_limite=None, estado=None):
    """Crea una tarjeta dentro de una lista."""
    return Tarjeta.create(
        id_lista=id_lista,
        titulo=titulo,
        descripcion=descripcion,
        fecha_limite=fecha_limite,
        estado=estado,
    )


def listado_tarjetas_por_lista(id_lista):
    """Lista las tarjetas de una lista concreta."""
    return (
        Tarjeta.select()
        .where(Tarjeta.id_lista == id_lista)
        .order_by(Tarjeta.id_tarjeta)
    )


def listado_tarjetas():
    """Lista todas las tarjetas."""
    return Tarjeta.select().order_by(Tarjeta.id_tarjeta)


def obtener_tarjeta_por_id(id_tarjeta):
    """Busca y retorna una tarjeta por ID."""
    return Tarjeta.get_or_none(Tarjeta.id_tarjeta == id_tarjeta)


def actualizar_tarjeta(
    id_tarjeta,
    id_lista=None,
    titulo=None,
    descripcion=SIN_CAMBIO,
    fecha_limite=SIN_CAMBIO,
    estado=SIN_CAMBIO,
):
    """Actualiza los campos indicados de una tarjeta."""
    tarjeta = obtener_tarjeta_por_id(id_tarjeta)
    if not tarjeta:
        return None
    if id_lista is not None:
        tarjeta.id_lista = id_lista
    if titulo is not None:
        tarjeta.titulo = titulo
    if descripcion is not SIN_CAMBIO:
        tarjeta.descripcion = descripcion
    if fecha_limite is not SIN_CAMBIO:
        tarjeta.fecha_limite = fecha_limite
    if estado is not SIN_CAMBIO:
        tarjeta.estado = estado
    tarjeta.save()
    return tarjeta


def eliminar_tarjeta(id_tarjeta):
    """Elimina físicamente una tarjeta por ID."""
    tarjeta = obtener_tarjeta_por_id(id_tarjeta)
    if not tarjeta:
        return False
    tarjeta.delete_instance()
    return True


def asignar_usuario_a_tarjeta(id_tarjeta, id_usuario):
    """Asigna un usuario a una tarjeta sin duplicar la relación."""
    asignacion, _ = AsignacionTarjeta.get_or_create(
        id_tarjeta=id_tarjeta, id_usuario=id_usuario
    )
    return asignacion


def listar_usuarios_asignados(id_tarjeta):
    """Lista los usuarios asignados a una tarjeta."""
    return (
        AsignacionTarjeta.select()
        .where(AsignacionTarjeta.id_tarjeta == id_tarjeta)
        .order_by(AsignacionTarjeta.id_usuario)
    )


def quitar_usuario_de_tarjeta(id_tarjeta, id_usuario):
    """Quita la asignación de un usuario a una tarjeta."""
    return (
        AsignacionTarjeta.delete()
        .where(
            (AsignacionTarjeta.id_tarjeta == id_tarjeta)
            & (AsignacionTarjeta.id_usuario == id_usuario)
        )
        .execute()
        > 0
    )


def crear_etiqueta(nombre, color):
    """Crea una etiqueta nueva."""
    return Etiqueta.create(nombre=nombre, color=color)


def listado_etiquetas():
    """Obtiene el listado de todas las etiquetas."""
    etiquetas = Etiqueta.select()
    if not etiquetas:
        print("No hay etiquetas registradas.")
    return etiquetas


def asignar_etiqueta_a_tarjeta(id_tarjeta, id_etiqueta):
    """Asigna una etiqueta a una tarjeta específica."""
    return TarjetaEtiqueta.create(id_tarjeta=id_tarjeta, id_etiqueta=id_etiqueta)