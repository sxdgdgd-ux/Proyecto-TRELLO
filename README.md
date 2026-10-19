# Gestor de proyectos Trello

Aplicación de consola para consultar y administrar proyectos, tableros, listas y
tarjetas almacenados en MySQL.

## Orden de los datos

Las entidades se organizan siguiendo sus relaciones:

1. **Proyecto**, **Usuario** y **Etiqueta**: datos base.
2. **ProyectoUsuario** y **Tablero**: vinculan usuarios y proyectos, y crean
   tableros dentro de un proyecto.
3. **Lista** y **Tarjeta**: cuelgan del tablero y de la lista, respectivamente.
4. **AsignacionTarjeta**, **Comentario** y **TarjetaEtiqueta**: relacionan
   tarjetas con usuarios y etiquetas.

El esquema completo está en [`Datos/sql/codigo.sql`](Datos/sql/codigo.sql).
Los listados muestran la jerarquía en ese mismo orden; las listas se ordenan por
posición y los registros relacionados de forma estable por nombre o identificador.

## Configuración y ejecución

Configura la conexión en un archivo `.env` local (no se incluye en Git) con las
variables `db`, `host`, `port`, `user` y `password`. Crea la base y sus tablas
ejecutando el script SQL y luego inicia:

- `python app.py`: consultas de usuarios, proyectos, tableros y tarjetas.
- `python menu.py`: creación y listado básico de proyectos.
