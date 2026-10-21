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

Los scripts del esquema están en `Datos/sql/`. Los listados muestran la
jerarquía en ese mismo orden; las listas se ordenan por posición y los registros
relacionados de forma estable por nombre o identificador.

## Organización del proyecto

- `Datos/conexion.py`: configuración, apertura y cierre de la conexión MySQL.
- `Datos/modelos/`: modelos que representan las entidades del sistema.
- `Datos/repositorio/`: operaciones de persistencia y consultas por entidad.
- `Datos/sql/`: scripts para crear la base y sus tablas.
- `negocio/`: reglas de negocio, validaciones y operaciones del sistema.
- `presentacion/`: menús de consola e interacción con el usuario.

La lógica auxiliar que existe actualmente pertenece a la presentación
(`presentacion/auxiliares.py`, con el nombre y la versión de la aplicación).
Las validaciones de negocio permanecen en `negocio/`; todavía no hay funciones
auxiliares compartidas propias de la capa de datos que justifiquen otro módulo.
Los archivos `conexion.py` y `models.py` en la raíz se conservan como fachadas
de compatibilidad; las implementaciones están dentro de `Datos/`.

## Configuración y ejecución

Configura la conexión en un archivo `.env` local (no se incluye en Git) con las
variables `db`, `host`, `port`, `user` y `password`. Crea la base y sus tablas
ejecutando uno de los scripts en `Datos/sql/` y luego inicia:

- `python app.py`: consultas de usuarios, proyectos, tableros y tarjetas.
- `python menu.py`: gestión interactiva de usuarios, proyectos, tableros,
  listas y tarjetas.
