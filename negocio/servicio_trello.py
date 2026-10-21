"""Validación de operaciones y permisos de negocio para proyectos/tableros."""
from datetime import date

from Datos.conexion import database
from Datos.modelos.models import (
    Etiqueta,
    Lista,
    Tablero,
    Usuario,
)
from Datos.repositorio import (
    repo_comentario,
    repo_etiqueta,
    repo_lista,
    repo_proyecto,
    repo_tablero,
    repo_tarjeta,
)

ROLES = ("Administrador", "Lider", "Miembro", "Observador")
ROLES_GESTION = ("Administrador", "Lider")
ROLES_EDICION_TARJETAS = (*ROLES_GESTION, "Miembro")


def _texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} es obligatorio.")
    return valor.strip()


def _id_positivo(valor, campo="ID"):
    if hasattr(valor, "get_id"):
        valor = valor.get_id()
    try:
        valor = int(valor)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{campo} debe ser un número entero.") from error
    if valor <= 0:
        raise ValueError(f"{campo} debe ser mayor que cero.")
    return valor


def _obtener_tablero(id_tablero):
    tablero = repo_tablero.obtener_tablero_por_id(_id_positivo(id_tablero, "Tablero"))
    if not tablero:
        raise ValueError("No existe el tablero indicado.")
    return tablero


def rol_en_tablero(id_tablero, id_usuario):
    """Busca primero el rol del tablero y luego el rol heredado del proyecto."""
    tablero = _obtener_tablero(id_tablero)
    usuario_id = _id_positivo(id_usuario, "Usuario")
    rol = repo_tablero.obtener_rol_usuario(tablero.id_tablero, usuario_id)
    if rol is None:
        rol = repo_proyecto.obtener_rol_usuario(tablero.id_proyecto, usuario_id)
    return rol


def exigir_rol_tablero(id_tablero, id_usuario, roles):
    rol = rol_en_tablero(id_tablero, id_usuario)
    if rol is None:
        raise PermissionError("El usuario no tiene acceso a este tablero.")
    if rol not in roles:
        raise PermissionError(f"El rol {rol} no permite realizar esta operación.")
    return rol


def crear_proyecto(nombre, descripcion, id_usuario):
    nombre = _texto(nombre, "El nombre del proyecto")
    usuario_id = _id_positivo(id_usuario, "Usuario")
    if not Usuario.get_or_none(Usuario.id_usuario == usuario_id):
        raise ValueError("No existe el usuario indicado.")
    with database.atomic():
        proyecto = repo_proyecto.crear_proyecto(nombre, descripcion or None)
        repo_proyecto.asignar_usuario_a_proyecto(
            proyecto.id_proyecto, usuario_id, "Administrador"
        )
    return proyecto


def crear_tablero(id_proyecto, titulo, id_usuario):
    proyecto_id = _id_positivo(id_proyecto, "Proyecto")
    usuario_id = _id_positivo(id_usuario, "Usuario")
    rol = repo_proyecto.obtener_rol_usuario(proyecto_id, usuario_id)
    if rol not in ROLES_GESTION:
        raise PermissionError("Solo un Administrador o Lider del proyecto puede crear tableros.")
    if not repo_proyecto.obtener_proyecto_por_id(proyecto_id):
        raise ValueError("No existe el proyecto indicado.")
    with database.atomic():
        tablero = repo_tablero.crear_tablero(proyecto_id, _texto(titulo, "El título"))
        repo_tablero.asignar_usuario_a_tablero(
            tablero.id_tablero, usuario_id, rol
        )
    return tablero


def actualizar_proyecto(id_proyecto, id_usuario, nombre=None, descripcion=None):
    proyecto_id = _id_positivo(id_proyecto, "Proyecto")
    usuario_id = _id_positivo(id_usuario, "Usuario")
    if repo_proyecto.obtener_rol_usuario(proyecto_id, usuario_id) not in ROLES_GESTION:
        raise PermissionError("Solo un Administrador o Lider puede editar el proyecto.")
    if nombre is not None:
        nombre = _texto(nombre, "El nombre del proyecto")
    return repo_proyecto.actualizar_proyecto(
        proyecto_id,
        nombre_proyecto=nombre,
        descripcion=(
            descripcion.strip() or None
            if descripcion is not None
            else repo_proyecto.SIN_CAMBIO
        ),
    )


def eliminar_proyecto(id_proyecto, id_usuario):
    proyecto_id = _id_positivo(id_proyecto, "Proyecto")
    usuario_id = _id_positivo(id_usuario, "Usuario")
    if repo_proyecto.obtener_rol_usuario(proyecto_id, usuario_id) not in ROLES_GESTION:
        raise PermissionError("Solo un Administrador o Lider puede eliminar el proyecto.")
    return repo_proyecto.eliminar_proyecto(proyecto_id)


def asignar_usuario_proyecto(id_proyecto, id_usuario, rol, id_actor):
    proyecto_id = _id_positivo(id_proyecto, "Proyecto")
    actor_id = _id_positivo(id_actor, "Usuario")
    usuario_id = _id_positivo(id_usuario, "Usuario")
    if repo_proyecto.obtener_rol_usuario(proyecto_id, actor_id) not in ROLES_GESTION:
        raise PermissionError("Solo un Administrador o Lider puede gestionar miembros.")
    if not Usuario.get_or_none(Usuario.id_usuario == usuario_id):
        raise ValueError("No existe el usuario indicado.")
    if rol not in ROLES:
        raise ValueError(f"Rol inválido. Valores permitidos: {', '.join(ROLES)}.")
    rol_actual = repo_proyecto.obtener_rol_usuario(proyecto_id, usuario_id)
    if rol_actual == "Administrador" and rol != "Administrador":
        administradores = sum(
            1
            for asignacion in repo_proyecto.listar_usuarios_proyecto(proyecto_id)
            if asignacion.rol == "Administrador"
        )
        if administradores <= 1:
            raise ValueError("El proyecto debe conservar al menos un Administrador.")
    return repo_proyecto.asignar_usuario_a_proyecto(proyecto_id, usuario_id, rol)


def eliminar_usuario_proyecto(id_proyecto, id_usuario, id_actor):
    proyecto_id = _id_positivo(id_proyecto, "Proyecto")
    actor_id = _id_positivo(id_actor, "Usuario")
    usuario_id = _id_positivo(id_usuario, "Usuario")
    if repo_proyecto.obtener_rol_usuario(proyecto_id, actor_id) not in ROLES_GESTION:
        raise PermissionError("Solo un Administrador o Lider puede gestionar miembros.")
    if repo_proyecto.obtener_rol_usuario(proyecto_id, usuario_id) == "Administrador":
        administradores = sum(
            1
            for asignacion in repo_proyecto.listar_usuarios_proyecto(proyecto_id)
            if asignacion.rol == "Administrador"
        )
        if administradores <= 1:
            raise ValueError("No se puede quitar al último Administrador del proyecto.")
    return repo_proyecto.eliminar_usuario_de_proyecto(proyecto_id, usuario_id)


def actualizar_tablero(id_tablero, id_usuario, titulo):
    tablero = _obtener_tablero(id_tablero)
    exigir_rol_tablero(tablero.id_tablero, id_usuario, ROLES_GESTION)
    return repo_tablero.actualizar_tablero(
        tablero.id_tablero, titulo=_texto(titulo, "El título")
    )


def eliminar_tablero(id_tablero, id_usuario):
    tablero = _obtener_tablero(id_tablero)
    exigir_rol_tablero(tablero.id_tablero, id_usuario, ROLES_GESTION)
    return repo_tablero.eliminar_tablero(tablero.id_tablero)


def asignar_usuario_tablero(id_tablero, id_usuario, rol, id_actor):
    tablero = _obtener_tablero(id_tablero)
    exigir_rol_tablero(tablero.id_tablero, id_actor, ROLES_GESTION)
    usuario_id = _id_positivo(id_usuario, "Usuario")
    if not Usuario.get_or_none(Usuario.id_usuario == usuario_id):
        raise ValueError("No existe el usuario indicado.")
    if rol not in ROLES:
        raise ValueError(f"Rol inválido. Valores permitidos: {', '.join(ROLES)}.")
    rol_actual = repo_tablero.obtener_rol_usuario(tablero.id_tablero, usuario_id)
    if rol_actual == "Administrador" and rol != "Administrador":
        administradores = sum(
            1
            for miembro in repo_tablero.listar_usuarios_tablero(tablero.id_tablero)
            if miembro.rol == "Administrador"
        )
        if administradores <= 1:
            raise ValueError("El tablero debe conservar al menos un Administrador.")
    return repo_tablero.asignar_usuario_a_tablero(
        tablero.id_tablero, usuario_id, rol
    )


def crear_comentario(id_tarjeta, id_usuario, texto):
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(_id_positivo(id_tarjeta, "Tarjeta"))
    if not tarjeta:
        raise ValueError("No existe la tarjeta indicada.")
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_EDICION_TARJETAS)
    return repo_comentario.crear_comentario(
        tarjeta.id_tarjeta, _id_positivo(id_usuario, "Usuario"),
        _texto(texto, "El comentario"),
    )


def eliminar_comentario(id_comentario, id_usuario):
    comentario = repo_comentario.obtener_comentario_por_id(
        _id_positivo(id_comentario, "Comentario")
    )
    if not comentario:
        raise ValueError("No existe el comentario indicado.")
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(comentario.id_tarjeta)
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    rol = exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_EDICION_TARJETAS)
    if comentario.id_usuario_id != int(id_usuario) and rol not in ROLES_GESTION:
        raise PermissionError("Solo puedes eliminar tus comentarios.")
    return repo_comentario.eliminar_comentario(comentario.id_comentario)


def actualizar_comentario(id_comentario, id_usuario, texto):
    comentario = repo_comentario.obtener_comentario_por_id(
        _id_positivo(id_comentario, "Comentario")
    )
    if not comentario:
        raise ValueError("No existe el comentario indicado.")
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(comentario.id_tarjeta)
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    rol = exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_EDICION_TARJETAS)
    if comentario.id_usuario_id != int(id_usuario) and rol not in ROLES_GESTION:
        raise PermissionError("Solo puedes editar tus comentarios.")
    return repo_comentario.actualizar_comentario(
        comentario.id_comentario, _texto(texto, "El comentario")
    )


def crear_etiqueta(nombre, color, id_tablero, id_usuario):
    exigir_rol_tablero(id_tablero, id_usuario, ROLES_GESTION)
    color = _texto(color, "El color")
    if len(color) > 20:
        raise ValueError("El color no puede superar los 20 caracteres.")
    return repo_etiqueta.crear_etiqueta(
        _texto(nombre, "El nombre de la etiqueta"), color
    )


def actualizar_etiqueta(id_etiqueta, nombre, color, id_tablero, id_usuario):
    exigir_rol_tablero(id_tablero, id_usuario, ROLES_GESTION)
    color = _texto(color, "El color")
    if len(color) > 20:
        raise ValueError("El color no puede superar los 20 caracteres.")
    etiqueta = repo_etiqueta.actualizar_etiqueta(
        _id_positivo(id_etiqueta, "Etiqueta"),
        _texto(nombre, "El nombre de la etiqueta"),
        color,
    )
    if not etiqueta:
        raise ValueError("No existe la etiqueta indicada.")
    return etiqueta


def eliminar_etiqueta(id_etiqueta, id_tablero, id_usuario):
    exigir_rol_tablero(id_tablero, id_usuario, ROLES_GESTION)
    if not repo_etiqueta.eliminar_etiqueta(_id_positivo(id_etiqueta, "Etiqueta")):
        raise ValueError("No existe la etiqueta indicada.")
    return True


def asignar_etiqueta(id_tarjeta, id_etiqueta, id_usuario):
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(_id_positivo(id_tarjeta, "Tarjeta"))
    if not tarjeta:
        raise ValueError("No existe la tarjeta indicada.")
    if not Etiqueta.get_or_none(
        Etiqueta.id_etiqueta == _id_positivo(id_etiqueta, "Etiqueta")
    ):
        raise ValueError("No existe la etiqueta indicada.")
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_EDICION_TARJETAS)
    return repo_etiqueta.asignar_etiqueta_a_tarjeta(
        tarjeta.id_tarjeta, int(id_etiqueta)
    )


def asignar_usuario_tarjeta(id_tarjeta, id_usuario, id_actor):
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(_id_positivo(id_tarjeta, "Tarjeta"))
    if not tarjeta:
        raise ValueError("No existe la tarjeta indicada.")
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    exigir_rol_tablero(lista.id_tablero, id_actor, ROLES_EDICION_TARJETAS)
    usuario_id = _id_positivo(id_usuario, "Usuario")
    if rol_en_tablero(lista.id_tablero, usuario_id) is None:
        raise ValueError("El usuario no pertenece al tablero.")
    return repo_tarjeta.asignar_usuario_a_tarjeta(tarjeta.id_tarjeta, usuario_id)


def quitar_usuario_tarjeta(id_tarjeta, id_usuario, id_actor):
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(_id_positivo(id_tarjeta, "Tarjeta"))
    if not tarjeta:
        raise ValueError("No existe la tarjeta indicada.")
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    exigir_rol_tablero(lista.id_tablero, id_actor, ROLES_EDICION_TARJETAS)
    return repo_tarjeta.quitar_usuario_de_tarjeta(
        tarjeta.id_tarjeta, _id_positivo(id_usuario, "Usuario")
    )


def eliminar_etiqueta_tarjeta(id_tarjeta, id_etiqueta, id_usuario):
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(_id_positivo(id_tarjeta, "Tarjeta"))
    if not tarjeta:
        raise ValueError("No existe la tarjeta indicada.")
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_EDICION_TARJETAS)
    return repo_etiqueta.eliminar_etiqueta_de_tarjeta(
        tarjeta.id_tarjeta, _id_positivo(id_etiqueta, "Etiqueta")
    )


def eliminar_usuario_tablero(id_tablero, id_usuario, id_actor):
    tablero = _obtener_tablero(id_tablero)
    exigir_rol_tablero(tablero.id_tablero, id_actor, ROLES_GESTION)
    usuario_id = _id_positivo(id_usuario, "Usuario")
    asignacion = repo_tablero.obtener_rol_usuario(tablero.id_tablero, usuario_id)
    if asignacion is None:
        return False
    if repo_proyecto.obtener_rol_usuario(tablero.id_proyecto, usuario_id) is not None:
        raise ValueError(
            "El usuario seguirá teniendo acceso por su rol en el proyecto. "
            "Cámbialo a Observador en este tablero o quítalo del proyecto."
        )
    if asignacion == "Administrador":
        administradores = sum(
            1
            for miembro in repo_tablero.listar_usuarios_tablero(tablero.id_tablero)
            if miembro.rol == "Administrador"
        )
        if administradores <= 1:
            raise ValueError("No se puede quitar al último Administrador del tablero.")
    return repo_tablero.eliminar_usuario_de_tablero(tablero.id_tablero, usuario_id)


def crear_lista(id_tablero, nombre, id_usuario, posicion=0):
    tablero = _obtener_tablero(id_tablero)
    exigir_rol_tablero(tablero.id_tablero, id_usuario, ROLES_GESTION)
    try:
        posicion = int(posicion)
    except (TypeError, ValueError) as error:
        raise ValueError("La posición debe ser un número entero.") from error
    return repo_lista.crear_lista(
        tablero.id_tablero, _texto(nombre, "El nombre de la lista"), posicion
    )


def actualizar_lista(id_lista, id_usuario, nombre=None, posicion=None):
    lista = repo_lista.obtener_lista_por_id(_id_positivo(id_lista, "Lista"))
    if not lista:
        raise ValueError("No existe la lista indicada.")
    exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_GESTION)
    if nombre is not None:
        nombre = _texto(nombre, "El nombre de la lista")
    if posicion is not None:
        try:
            posicion = int(posicion)
        except (TypeError, ValueError) as error:
            raise ValueError("La posición debe ser un número entero.") from error
    return repo_lista.actualizar_lista(lista.id_lista, nombre, posicion)


def eliminar_lista(id_lista, id_usuario):
    lista = repo_lista.obtener_lista_por_id(_id_positivo(id_lista, "Lista"))
    if not lista:
        raise ValueError("No existe la lista indicada.")
    exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_GESTION)
    return repo_lista.eliminar_lista(lista.id_lista)


def crear_tarjeta(id_lista, titulo, descripcion, estado, fecha_limite, id_usuario):
    lista = repo_lista.obtener_lista_por_id(_id_positivo(id_lista, "Lista"))
    if not lista:
        raise ValueError("No existe la lista indicada.")
    exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_EDICION_TARJETAS)
    fecha = _fecha(fecha_limite)
    return repo_tarjeta.crear_tarjeta(
        lista.id_lista,
        _texto(titulo, "El título"),
        descripcion.strip() or None if descripcion else None,
        fecha,
        estado.strip() or "Pendiente" if estado else "Pendiente",
    )


def _fecha(valor):
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        return None
    if isinstance(valor, date):
        return valor
    try:
        return date.fromisoformat(valor.strip())
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("La fecha límite debe tener formato AAAA-MM-DD.") from error


def actualizar_tarjeta(
    id_tarjeta, id_usuario, titulo=None, descripcion=None, estado=None, fecha_limite=None
):
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(_id_positivo(id_tarjeta, "Tarjeta"))
    if not tarjeta:
        raise ValueError("No existe la tarjeta indicada.")
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_EDICION_TARJETAS)
    return repo_tarjeta.actualizar_tarjeta(
        tarjeta.id_tarjeta,
        titulo=_texto(titulo, "El título") if titulo is not None else None,
        descripcion=(
            descripcion.strip() or None
            if descripcion is not None
            else repo_tarjeta.SIN_CAMBIO
        ),
        estado=(
            _texto(estado, "El estado")
            if estado is not None
            else repo_tarjeta.SIN_CAMBIO
        ),
        fecha_limite=(
            _fecha(fecha_limite)
            if fecha_limite is not None
            else repo_tarjeta.SIN_CAMBIO
        ),
    )


def eliminar_tarjeta(id_tarjeta, id_usuario):
    tarjeta = repo_tarjeta.obtener_tarjeta_por_id(_id_positivo(id_tarjeta, "Tarjeta"))
    if not tarjeta:
        raise ValueError("No existe la tarjeta indicada.")
    lista = repo_lista.obtener_lista_por_id(tarjeta.id_lista)
    exigir_rol_tablero(lista.id_tablero, id_usuario, ROLES_GESTION)
    return repo_tarjeta.eliminar_tarjeta(tarjeta.id_tarjeta)


def listar_tableros_usuario(id_usuario):
    usuario_id = _id_positivo(id_usuario, "Usuario")
    if not Usuario.get_or_none(Usuario.id_usuario == usuario_id):
        raise ValueError("No existe el usuario indicado.")
    return [
        tablero
        for tablero in Tablero.select().order_by(Tablero.id_tablero)
        if rol_en_tablero(tablero.id_tablero, usuario_id) is not None
    ]


def obtener_rol_tablero(id_tablero, id_usuario):
    rol = rol_en_tablero(id_tablero, id_usuario)
    if rol is None:
        raise PermissionError("El usuario no tiene acceso a este tablero.")
    return rol
