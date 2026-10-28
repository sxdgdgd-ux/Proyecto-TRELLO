"""Operaciones de negocio para la gestión de usuarios."""

import re

from Datos.repositorio import repo_usuario

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_LONGITUD_NOMBRE = 100
MAX_LONGITUD_EMAIL = 150


def procesar_listado_usuario():
    """Muestra todos los usuarios registrados."""
    usuarios = list(repo_usuario.listado_usuarios())
    if not usuarios:
        return

    print("\n--- USUARIOS ---")
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario} | {usuario.nombre} | {usuario.email}")


def crear_usuario(nombre: str, email: str):
    """Valida y crea un usuario o recupera el existente con el mismo correo."""
    nombre = nombre.strip() if isinstance(nombre, str) else ""
    email = email.strip().lower() if isinstance(email, str) else ""

    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if len(nombre) > MAX_LONGITUD_NOMBRE:
        raise ValueError(
            f"El nombre no puede superar {MAX_LONGITUD_NOMBRE} caracteres."
        )
    if len(email) > MAX_LONGITUD_EMAIL:
        raise ValueError(
            f"El correo no puede superar {MAX_LONGITUD_EMAIL} caracteres."
        )
    if not PATRON_EMAIL.fullmatch(email):
        raise ValueError("Ingresa un correo válido, por ejemplo nombre@dominio.com.")

    return repo_usuario.crear_usuario(nombre, email)
