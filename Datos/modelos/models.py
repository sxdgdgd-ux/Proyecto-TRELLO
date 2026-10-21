from datetime import date, datetime

from peewee import (
    AutoField,
    CharField,
    CompositeKey,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)
from peewee import PeeweeException

from Datos.conexion import database


class BaseModel(Model):
    class Meta:
        database = database


class Proyecto(BaseModel):
    id_proyecto = AutoField()
    nombre_proyecto = CharField(max_length=100)
    descripcion = TextField(null=True)
    fecha_creacion = DateField(default=date.today)

    class Meta:
        table_name = "proyecto"


class Usuario(BaseModel):
    id_usuario = AutoField()
    nombre = CharField(max_length=100)
    email = CharField(max_length=150, unique=True)

    class Meta:
        table_name = "usuario"


class Etiqueta(BaseModel):
    id_etiqueta = AutoField()
    nombre = CharField(max_length=50)
    color = CharField(max_length=20, default="#808080")

    class Meta:
        table_name = "etiqueta"


class ProyectoUsuario(BaseModel):
    id_proyecto = ForeignKeyField(
        Proyecto, column_name="id_proyecto", on_delete="CASCADE"
    )
    id_usuario = ForeignKeyField(
        Usuario, column_name="id_usuario", on_delete="CASCADE"
    )
    rol = CharField(max_length=20, default="Miembro")

    class Meta:
        table_name = "proyecto_usuario"
        primary_key = CompositeKey("id_proyecto", "id_usuario")


class Tablero(BaseModel):
    id_tablero = AutoField()
    id_proyecto = ForeignKeyField(
        Proyecto, column_name="id_proyecto", on_delete="CASCADE"
    )
    titulo = CharField(max_length=100)

    class Meta:
        table_name = "tablero"


class TableroUsuario(BaseModel):
    id_tablero = ForeignKeyField(
        Tablero, column_name="id_tablero", on_delete="CASCADE"
    )
    id_usuario = ForeignKeyField(
        Usuario, column_name="id_usuario", on_delete="CASCADE"
    )
    rol = CharField(max_length=20, default="Miembro")

    class Meta:
        table_name = "tablero_usuario"
        primary_key = CompositeKey("id_tablero", "id_usuario")


class Lista(BaseModel):
    id_lista = AutoField()
    id_tablero = ForeignKeyField(
        Tablero, column_name="id_tablero", on_delete="CASCADE"
    )
    nombre_lista = CharField(max_length=100)
    posicion = IntegerField(default=0)

    class Meta:
        table_name = "lista"


class Tarjeta(BaseModel):
    id_tarjeta = AutoField()
    id_lista = ForeignKeyField(
        Lista, column_name="id_lista", on_delete="CASCADE"
    )
    titulo = CharField(max_length=150)
    descripcion = TextField(null=True)
    fecha_limite = DateField(null=True)
    estado = CharField(max_length=50, default="Pendiente")

    class Meta:
        table_name = "tarjeta"


class AsignacionTarjeta(BaseModel):
    id_tarjeta = ForeignKeyField(
        Tarjeta, column_name="id_tarjeta", on_delete="CASCADE"
    )
    id_usuario = ForeignKeyField(
        Usuario, column_name="id_usuario", on_delete="CASCADE"
    )

    class Meta:
        table_name = "asignacion_tarjeta"
        primary_key = CompositeKey("id_tarjeta", "id_usuario")


class Comentario(BaseModel):
    id_comentario = AutoField()
    id_tarjeta = ForeignKeyField(
        Tarjeta, column_name="id_tarjeta", on_delete="CASCADE"
    )
    id_usuario = ForeignKeyField(
        Usuario, column_name="id_usuario", on_delete="CASCADE"
    )
    texto = TextField()
    fecha_creacion = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "comentario"


class TarjetaEtiqueta(BaseModel):
    id_tarjeta = ForeignKeyField(
        Tarjeta, column_name="id_tarjeta", on_delete="CASCADE"
    )
    id_etiqueta = ForeignKeyField(
        Etiqueta, column_name="id_etiqueta", on_delete="CASCADE"
    )

    class Meta:
        table_name = "tarjeta_etiqueta"
        primary_key = CompositeKey("id_tarjeta", "id_etiqueta")


def crear_tablas():
    try:
        with database:
            database.create_tables(
                [
                    Proyecto,
                    Usuario,
                    Etiqueta,
                    ProyectoUsuario,
                    Tablero,
                    TableroUsuario,
                    Lista,
                    Tarjeta,
                    AsignacionTarjeta,
                    Comentario,
                    TarjetaEtiqueta,
                ]
            )
        return True
    except (PeeweeException, OSError) as error:
        print(
            "No se pudo conectar a MySQL ni preparar las tablas. "
            "Verifica que XAMPP/MySQL esté encendido y la configuración "
            f"del .env: {error}"
        )
        return False