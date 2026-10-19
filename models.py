"""Compatibilidad para importar los modelos desde el modulo principal."""
from Datos.modelos.models import (
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

__all__ = [
    "AsignacionTarjeta",
    "BaseModel",
    "Comentario",
    "Etiqueta",
    "Lista",
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
