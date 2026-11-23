"""Configuración y ciclo de vida de la conexión a la base de datos."""
from decouple import config
from peewee import MySQLDatabase, PeeweeException

database = MySQLDatabase(
    config("db", default="trello_db"),
    charset="utf8mb4",
    host=config("host", default="localhost"),
    port=config("port", default=3306, cast=int),
    user=config("user", default="root"),
    password=config("password", default=""),
)


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


__all__ = ["cerrar_bd", "conectar_bd", "database"]
