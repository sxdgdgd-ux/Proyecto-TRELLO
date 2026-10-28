"""Operaciones de negocio para la gestión de usuarios."""

from Datos.repositorio import repo_usuario


def procesar_listado_usuario():
    """Muestra todos los usuarios registrados."""
    usuarios = list(repo_usuario.listado_usuarios())
    if not usuarios:
        return

    print("\n--- USUARIOS ---")
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario} | {usuario.nombre} | {usuario.email}")


def crear_usuario(nombre: str, email: str):
    """Crea un usuario o recupera el existente con el mismo correo."""
    return repo_usuario.crear_usuario(nombre, email)
