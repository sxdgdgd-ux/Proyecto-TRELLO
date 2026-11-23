"""Configuración compartida por todos los modelos ORM."""

from peewee import Model

from datos.conexion import database


class ModelBase(Model):
    class Meta:
        database = database
