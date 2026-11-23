"""Compatibilidad con las importaciones antiguas de la conexión."""
from datos.conexion import cerrar_bd, conectar_bd, database
from datos.model_base import ModelBase
from datos.modelos.models import BaseModel

__all__ = ["BaseModel", "ModelBase", "cerrar_bd", "conectar_bd", "database"]
