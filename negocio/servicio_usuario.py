"""Operaciones de negocio para la gestión de usuarios."""

import re

from decouple import config
from auxiliares.seguridad import (
    hashear_contrasena,
    verificar_contrasena,
    verificar_hash_anterior,
)
from Datos.repositorio import repo_usuario

PATRON_EMAIL = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)
PATRON_CONTRASENA = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9\s])\S{8,128}$"
)
MAX_LONGITUD_NOMBRE = 100


def procesar_listado_usuario(id_actor: int):
    """Obtiene una lectura actualizada de los usuarios registrados."""
    exigir_administrador(id_actor)
    return repo_usuario.listado_usuarios()


def validar_email(email: str) -> str:
    """Normaliza y valida el correo electrónico."""
    email = email.strip().lower() if isinstance(email, str) else ""
    if not PATRON_EMAIL.fullmatch(email):
        raise ValueError("Ingresa un correo válido, por ejemplo nombre@dominio.com.")
    return email


def validar_contrasena(contrasena: str) -> str:
    """Exige una contraseña segura con longitud y tipos de caracteres mínimos."""
    if not isinstance(contrasena, str) or not PATRON_CONTRASENA.fullmatch(contrasena):
        raise ValueError(
            "La contraseña debe tener entre 8 y 128 caracteres, incluir "
            "mayúscula, minúscula, número y símbolo, y no contener espacios."
        )
    return contrasena


def _crear_hash_contrasena(contrasena: str) -> str:
    return hashear_contrasena(contrasena)


def crear_usuario(nombre: str, email: str, contrasena: str):
    """Valida y crea un usuario con una contraseña almacenada como hash."""
    nombre = nombre.strip() if isinstance(nombre, str) else ""

    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if len(nombre) > MAX_LONGITUD_NOMBRE:
        raise ValueError(
            f"El nombre no puede superar {MAX_LONGITUD_NOMBRE} caracteres."
        )
    email = validar_email(email)
    validar_contrasena(contrasena)

    if repo_usuario.obtener_usuario_por_email(email):
        raise ValueError("Ya existe un usuario registrado con ese correo.")
    return repo_usuario.crear_usuario(
        nombre, email, _crear_hash_contrasena(contrasena)
    )


def autenticar_usuario(id_usuario: int, contrasena: str) -> bool:
    """Comprueba la contraseña y migra hashes PBKDF2 válidos a bcrypt."""
    usuario = repo_usuario.obtener_usuario_por_id(id_usuario)
    if not usuario or not usuario.password_hash or not isinstance(contrasena, str):
        return False

    hash_guardado = usuario.password_hash
    if hash_guardado.startswith("pbkdf2_sha256$"):
        if not verificar_hash_anterior(contrasena, hash_guardado):
            return False
        repo_usuario.actualizar_usuario(
            usuario.id_usuario, password_hash=_crear_hash_contrasena(contrasena)
        )
        return True
    return verificar_contrasena(contrasena, hash_guardado)


def actualizar_usuario(
    id_usuario: int,
    id_actor: int,
    nombre: str = None,
    email: str = None,
    contrasena: str = None,
):
    """Permite a un administrador actualizar los datos de una cuenta."""
    exigir_administrador(id_actor)
    cambios = {}
    if nombre is not None:
        nombre = nombre.strip() if isinstance(nombre, str) else ""
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if len(nombre) > MAX_LONGITUD_NOMBRE:
            raise ValueError(
                f"El nombre no puede superar {MAX_LONGITUD_NOMBRE} caracteres."
            )
        cambios["nombre"] = nombre
    if email is not None:
        cambios["email"] = validar_email(email)
    if contrasena is not None:
        validar_contrasena(contrasena)
        cambios["password_hash"] = _crear_hash_contrasena(contrasena)
    return repo_usuario.actualizar_usuario(id_usuario, **cambios)


def es_administrador(id_usuario: int) -> bool:
    """Indica si la cuenta existe y tiene el rol administrativo global."""
    usuario = repo_usuario.obtener_usuario_por_id(id_usuario)
    return bool(usuario and usuario.es_admin)


def exigir_administrador(id_usuario: int):
    """Impide que cuentas comunes administren otras cuentas."""
    if not es_administrador(id_usuario):
        raise PermissionError("Solo un administrador puede gestionar usuarios.")


def eliminar_usuario(id_usuario: int, id_actor: int) -> bool:
    """Elimina una cuenta sin permitir quitar al último administrador."""
    exigir_administrador(id_actor)
    usuario = repo_usuario.obtener_usuario_por_id(id_usuario)
    if not usuario:
        return False
    if usuario.es_admin:
        administradores = sum(
            cuenta.es_admin for cuenta in repo_usuario.listado_usuarios()
        )
        if administradores <= 1:
            raise ValueError("No se puede eliminar al último administrador.")
    return repo_usuario.eliminar_usuario(id_usuario)


def bootstrap_administrador(nombre: str, email: str, contrasena: str):
    """Crea o habilita el administrador indicado explícitamente en .env."""
    email = validar_email(email)
    email_configurado = config("admin_email", default="").strip().lower()
    if not email_configurado or email != email_configurado:
        raise ValueError(
            "El correo debe coincidir con la variable admin_email configurada localmente."
        )
    nombre = nombre.strip() if isinstance(nombre, str) else ""
    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if len(nombre) > MAX_LONGITUD_NOMBRE:
        raise ValueError(
            f"El nombre no puede superar {MAX_LONGITUD_NOMBRE} caracteres."
        )
    validar_contrasena(contrasena)
    if any(cuenta.es_admin for cuenta in repo_usuario.listado_usuarios()):
        raise ValueError(
            "Ya existe un administrador. El alta inicial solo se permite una vez."
        )

    usuario = repo_usuario.obtener_usuario_por_email(email)
    hash_nuevo = _crear_hash_contrasena(contrasena)
    if usuario:
        return repo_usuario.actualizar_usuario(
            usuario.id_usuario,
            nombre=nombre,
            password_hash=hash_nuevo,
            es_admin=True,
        )
    return repo_usuario.crear_usuario(nombre, email, hash_nuevo, es_admin=True)
