"""Funciones de hashing y verificación de contraseñas."""

import hashlib
import hmac

import bcrypt


_PREFIJO_HASH = b"Proyecto-TRELLO bcrypt-sha256\x00"


def _entrada_bcrypt(contrasena: str) -> bytes:
    """Prehashea la contraseña para evitar el límite de 72 bytes de bcrypt."""
    return hashlib.sha256(_PREFIJO_HASH + contrasena.encode("utf-8")).digest()


def hashear_contrasena(contrasena: str) -> str:
    """Genera un hash bcrypt no reversible, con una sal aleatoria."""
    return bcrypt.hashpw(_entrada_bcrypt(contrasena), bcrypt.gensalt()).decode("utf-8")


def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    """Comprueba una contraseña contra un hash bcrypt."""
    if not isinstance(contrasena, str) or not isinstance(hash_guardado, str):
        return False
    try:
        return bcrypt.checkpw(
            _entrada_bcrypt(contrasena), hash_guardado.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def verificar_hash_anterior(contrasena: str, hash_guardado: str) -> bool:
    """Verifica hashes PBKDF2 previos para migrarlos a bcrypt al iniciar sesión."""
    try:
        algoritmo, iteraciones, sal_hex, hash_hex = hash_guardado.split("$")
        if algoritmo != "pbkdf2_sha256":
            return False
        iteraciones = int(iteraciones)
        sal = bytes.fromhex(sal_hex)
        hash_esperado = bytes.fromhex(hash_hex)
    except (AttributeError, TypeError, ValueError):
        return False
    if iteraciones != 600_000 or len(hash_esperado) != 32:
        return False
    hash_calculado = hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode("utf-8"), sal, iteraciones
    )
    return hmac.compare_digest(hash_calculado, hash_esperado)
