"""Compatibilidad para importar los modelos desde el modulo principal."""
from datos.modelos.models import (
    AsignacionTarjeta,
    BaseModel,
    Comentario,
    Etiqueta,
    Lista,
    Proyecto,
    ProyectoUsuario,
    Tablero,
    TableroUsuario,
    Tarjeta,
    TarjetaEtiqueta,
    Usuario,
    crear_tablas,
    database,
)
from datos.model_base import ModelBase

__all__ = [
    "AsignacionTarjeta",
    "BaseModel",
    "Comentario",
    "Etiqueta",
    "Lista",
    "ModelBase",
    "Proyecto",
    "ProyectoUsuario",
    "Tablero",
    "TableroUsuario",
    "Tarjeta",
    "TarjetaEtiqueta",
    "Usuario",
    "crear_tablas",
    "database",
]
