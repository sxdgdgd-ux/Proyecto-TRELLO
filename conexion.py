"""Compatibilidad para importar la conexion compartida de la aplicacion."""
from peewee import PeeweeException

from Datos.modelos.models import BaseModel, database


def conectar_bd():
    """Abre la conexión y comunica claramente si MySQL no está disponible."""
    try:
        if database.is_closed():
            database.connect()
        return True
    except (PeeweeException, OSError) as error:
        print(
            "No se pudo conectar a MySQL. Verifica que XAMPP/MySQL esté "
            f"encendido y que la configuración del .env sea correcta: {error}"
        )
        return False


def cerrar_bd():
    """Cierra la conexión compartida si está abierta."""
    if not database.is_closed():
        database.close()


__all__ = ["BaseModel", "cerrar_bd", "conectar_bd", "database"]
