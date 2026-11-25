# Gestor de proyectos Trello

Aplicación de consola para consultar y administrar proyectos, tableros, listas y
tarjetas almacenados en MySQL.

## Integrantes

Alejandro Ortiz
Diego Araya
Fabian Rojas

## Descripción

Gestor multicapa de proyectos tipo Trello. La persistencia usa Peewee y MySQL;
la aplicación permite administrar usuarios, proyectos, tableros, listas,
tarjetas, etiquetas y comentarios. El acceso al menú está protegido por login.

## Orden de los datos

Las entidades se organizan siguiendo sus relaciones:

1. **Proyecto**, **Usuario** y **Etiqueta**: datos base.
2. **ProyectoUsuario** y **Tablero**: vinculan usuarios y proyectos, y crean
   tableros dentro de un proyecto.
3. **Lista** y **Tarjeta**: cuelgan del tablero y de la lista, respectivamente.
4. **AsignacionTarjeta**, **Comentario** y **TarjetaEtiqueta**: relacionan
   tarjetas con usuarios y etiquetas.

Los scripts del esquema están en `datos/sql/`. Los listados muestran la
jerarquía en ese mismo orden; las listas se ordenan por posición y los registros
relacionados de forma estable por nombre o identificador.

## Organización del proyecto

- `datos/conexion.py`: configuración, apertura y cierre de la conexión MySQL.
- `datos/model_base.py`: configuración compartida de los modelos Peewee.
- `datos/modelos/`: modelos que representan las entidades del sistema.
- `datos/repositorio/`: operaciones de persistencia y consultas por entidad.
- `datos/sql/`: scripts para crear la base y sus tablas.
- `negocio/`: reglas de negocio, validaciones y operaciones del sistema.
- `presentacion/`: menús de consola e interacción con el usuario.
- `auxiliares/seguridad.py`: hashing/verificación bcrypt y verificación
  transitoria de hashes PBKDF2 antiguos. Maskpass oculta las contraseñas durante
  el ingreso.

La configuración reutilizable está en `auxiliares/configuracion.py`; los
mensajes comunes están en `auxiliares/mensajes.py`. Las validaciones de negocio
permanecen en `negocio/` y los formatos de tabla pertenecen a la presentación.
Los archivos `conexion.py` y `models.py` en la raíz se conservan como fachadas
de compatibilidad; las implementaciones están dentro de `datos/`.

## Dependencias

Python 3, Peewee, PyMySQL, python-decouple, prettytable, bcrypt y maskpass.
Instálalas desde la raíz del proyecto:

- `python -m pip install -r requirements.txt`

## Configuración y ejecución

Configura la conexión en un archivo `.env` local (no se incluye en Git) con las
variables `db`, `host`, `port`, `user` y `password`. Para el primer
administrador, también configura `admin_email`.

Puedes copiar `.env.example` y ajustar sus valores:

```env
db=trello_db
host=localhost
port=8080
user=root
password=
admin_email=administrador@ejemplo.com
```

Mantén el valor de `port` igual al puerto real configurado en tu MySQL/XAMPP.
Este proyecto usa `8080` en la configuración local actual cuando 3306 no está
disponible; no requiere que el puerto coincida con el puerto HTTP de XAMPP.

Crea la base y sus tablas ejecutando `datos/sql/trello_db.sql` desde MySQL/XAMPP
o usando el script compatible disponible en `datos/sql/`.

Al iniciar, la aplicación crea las tablas que falten y agrega automáticamente
las columnas `password_hash`, `es_admin` y `activo` a una tabla `usuario`
existente. La cuenta de MySQL debe tener permisos para modificar el esquema; de
lo contrario, aplica una sola vez
`datos/sql/migracion_contrasena_usuario.sql` sobre una base que todavía no tenga
esas columnas.

El registro valida el formato del correo y exige una contraseña de 8 a 128
caracteres con mayúscula, minúscula, número y símbolo. Antes de registrarla, la
solicita dos veces. Las contraseñas se guardan como hashes bcrypt con sal
aleatoria (no se pueden desencriptar); se aplica un prehash SHA-256 antes de
bcrypt para conservar la política de longitud sin el límite de 72 bytes de
bcrypt. Los hashes PBKDF2 creados por versiones anteriores se verifican y
actualizan a bcrypt al iniciar sesión correctamente.

Las cuentas antiguas cuyo `password_hash` sea nulo quedan bloqueadas hasta que
un administrador restablezca su contraseña. Para designar al primer
administrador, agrega `admin_email` al `.env` con el correo que el operador
local autoriza y ejecuta `python main.py --bootstrap-admin`. Este comando
solicita nombre y contraseña, crea esa cuenta o restablece la cuenta existente
con ese correo y le asigna el rol administrativo. Solo funciona cuando aún no
hay ningún administrador; los usuarios normales no pueden asignarse ese rol.
Una vez inicializado, la gestión de cuentas está disponible solo para
administradores. Las cuentas se pueden deshabilitar y reactivar sin borrar su
historial; el login rechaza las cuentas deshabilitadas y no se puede
deshabilitar al último administrador activo. No compartas
el `.env` ni permitas que usuarios no confiables ejecuten el comando de
bootstrap en el equipo del servidor.

- `python main.py`: solicita autenticación y abre el menú principal de gestión
  y consultas.
- `python app.py`: alias del inicio autenticado de `main.py`.
- `python menu.py`: gestión interactiva de usuarios, proyectos, tableros,
  listas y tarjetas.

## Usuario inicial

Antes del primer uso define `admin_email` en `.env` y ejecuta:

```powershell
python main.py --bootstrap-admin
```

El programa solicitará el nombre del administrador, el correo configurado,
una contraseña segura y su confirmación. No guardes el usuario ni la contraseña
en el código fuente ni compartas el archivo `.env`.
