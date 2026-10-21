"""Compatibilidad con las importaciones antiguas de la conexión."""
from Datos.conexion import cerrar_bd, conectar_bd, database
from Datos.modelos.models import BaseModel

__all__ = ["BaseModel", "cerrar_bd", "conectar_bd", "database"]
