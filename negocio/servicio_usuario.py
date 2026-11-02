"""Operaciones de negocio para la gestión de usuarios."""

import hashlib
import hmac
import re
import secrets

from Datos.repositorio import repo_usuario

PATRON_EMAIL = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}$"
)
PATRON_CONTRASENA = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9\s])\S{8,128}$"
)
MAX_LONGITUD_NOMBRE = 100
MAX_LONGITUD_EMAIL = 150
ITERACIONES_HASH = 600_000


def procesar_listado_usuario():
    """Obtiene una lectura actualizada de los usuarios registrados."""
    return repo_usuario.listado_usuarios()


def validar_email(email: str) -> str:
    """Normaliza y valida el correo electrónico."""
    email = email.strip().lower() if isinstance(email, str) else ""
    if len(email) > MAX_LONGITUD_EMAIL:
        raise ValueError(
            f"El correo no puede superar {MAX_LONGITUD_EMAIL} caracteres."
        )
    local, separador, _ = email.partition("@")
    if (
        not separador
        or local.startswith(".")
        or local.endswith(".")
        or ".." in local
        or not PATRON_EMAIL.fullmatch(email)
    ):
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
    sal = secrets.token_bytes(16)
    hash_contrasena = hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode("utf-8"), sal, ITERACIONES_HASH
    )
    return (
        f"pbkdf2_sha256${ITERACIONES_HASH}${sal.hex()}$"
        f"{hash_contrasena.hex()}"
    )


def _verificar_hash_contrasena(contrasena: str, hash_guardado: str) -> bool:
    try:
        algoritmo, iteraciones, sal_hex, hash_hex = hash_guardado.split("$")
        if algoritmo != "pbkdf2_sha256" or int(iteraciones) != ITERACIONES_HASH:
            return False
        sal = bytes.fromhex(sal_hex)
        hash_esperado = bytes.fromhex(hash_hex)
    except (AttributeError, ValueError):
        return False
    if len(sal) != 16 or len(hash_esperado) != 32:
        return False

    hash_calculado = hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode("utf-8"), sal, ITERACIONES_HASH
    )
    return hmac.compare_digest(hash_calculado, hash_esperado)


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
    """Comprueba la contraseña de un usuario existente."""
    usuario = repo_usuario.obtener_usuario_por_id(id_usuario)
    return bool(
        usuario
        and usuario.password_hash
        and isinstance(contrasena, str)
        and _verificar_hash_contrasena(contrasena, usuario.password_hash)
    )


def establecer_contrasena(id_usuario: int, contrasena: str):
    """Guarda de forma segura una contraseña nueva para un usuario."""
    validar_contrasena(contrasena)
    return repo_usuario.actualizar_usuario(
        id_usuario, password_hash=_crear_hash_contrasena(contrasena)
    )


def actualizar_usuario(
    id_usuario: int,
    nombre: str = None,
    email: str = None,
    contrasena: str = None,
):
    """Valida y actualiza los datos indicados de un usuario."""
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
