from peewee import AutoField, CharField, ForeignKeyField, CompositeKey
from ..conexion import BaseModel
from Datos.modelos.tarjeta import Tarjeta

class Etiqueta(BaseModel):
    id_etiqueta = AutoField()
    nombre = CharField(max_length=50)
    color = CharField(max_length=20)

    class Meta:
        table_name = 'etiqueta'

class TarjetaEtiqueta(BaseModel):
    id_etiqueta = ForeignKeyField(Etiqueta, column_name='id_etiqueta', field='id_etiqueta', on_delete='CASCADE')
    id_tarjeta = ForeignKeyField(Tarjeta, column_name='id_tarjeta', field='id_tarjeta', on_delete='CASCADE')

    class Meta:
        table_name = 'tarjeta_etiqueta'
        indexes = ((('id_tarjeta', 'id_etiqueta'), True),)
        primary_key = CompositeKey('id_etiqueta', 'id_tarjeta')