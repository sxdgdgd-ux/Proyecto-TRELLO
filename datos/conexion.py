"""Configuración y ciclo de vida de la conexión a la base de datos."""
from decouple import config
from peewee import MySQLDatabase, PeeweeException
from auxiliares.configuracion import (
    DB_HOST_DEFAULT,
    DB_NAME_DEFAULT,
    DB_PORT_DEFAULT,
)
from auxiliares.mensajes import DB_NO_DISPONIBLE

database = MySQLDatabase(
    config("db", default=DB_NAME_DEFAULT),
    charset="utf8mb4",
    host=config("host", default=DB_HOST_DEFAULT),
    port=config("port", default=DB_PORT_DEFAULT, cast=int),
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
        print(f"{DB_NO_DISPONIBLE} Detalle: {error}")
        return False


def cerrar_bd():
    """Cierra la conexión compartida si está abierta."""
    if not database.is_closed():
        database.close()


__all__ = ["cerrar_bd", "conectar_bd", "database"]
