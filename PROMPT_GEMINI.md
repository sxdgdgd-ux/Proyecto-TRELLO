# Prompt para analizar este proyecto con Gemini

Copia y pega el siguiente prompt en Gemini y adjunta el repositorio o los
archivos del proyecto. No compartas el contenido de `.env` ni credenciales.

---

Actúa como un ingeniero de software senior especializado en Python, Peewee y
MySQL. Analiza el código que te proporcionaré teniendo en cuenta este contexto
real del proyecto. Responde en español, distingue los problemas comprobados de
las recomendaciones y no inventes funcionalidades que no aparezcan en el
código.

## Descripción

Este proyecto, **Gestor de Proyectos Trello**, es una aplicación de consola
para registrar usuarios y administrar proyectos, tableros, listas, tarjetas y
sus datos relacionados. Persiste la información en MySQL y está organizado en
capas de presentación, negocio y acceso a datos. No es una aplicación web ni
usa la API de Trello.

## Tecnologías y ejecución

- Python.
- Peewee como ORM y PyMySQL como controlador MySQL.
- `python-decouple` para leer la configuración local.
- PrettyTable para mostrar resultados en tablas de consola.
- Dependencias instalables desde `requirements.txt`.
- `python main.py`: menú inicial para elegir gestión o consultas.
- `python menu.py`: entrada directa al menú de gestión.
- `python app.py`: entrada directa al menú de consultas.

La conexión se configura con un archivo `.env` local en la raíz y las claves
`db`, `host`, `port`, `user`, `password` y opcionalmente `admin_email`. El
archivo es local y no se debe incluir, mostrar ni modificar como parte de una
revisión. El esquema está en `Datos/sql/trello_db.sql` y `Datos/sql/codigo.sql`;
la migración explícita de contraseñas y del rol global está en
`Datos/sql/migracion_contrasena_usuario.sql`. Al iniciar, el programa también
crea las tablas que falten y agrega las columnas `password_hash` y `es_admin` a
una tabla `usuario` existente si hacen falta.

## Organización del código

- `main.py`, `menu.py` y `app.py`: puntos de entrada.
- `presentacion/`: menús, entradas del usuario y salida de consola.
- `negocio/`: validaciones, operaciones de dominio y permisos.
- `auxiliares/seguridad.py`: hashing bcrypt y compatibilidad temporal para
  verificar hashes PBKDF2 existentes.
- `Datos/modelos/`: modelos Peewee y creación/migración de tablas.
- `Datos/repositorio/`: consultas y operaciones de persistencia por entidad.
- `Datos/sql/`: creación y migración del esquema MySQL.
- `conexion.py` y `models.py` en la raíz: fachadas de compatibilidad; las
  implementaciones principales están en `Datos/`.

Respeta esta separación al proponer cambios: la presentación debe delegar las
reglas en `negocio/`, y el negocio debe usar los repositorios/modelos para la
persistencia. Conserva los nombres de tablas y columnas existentes y comprueba
la coherencia entre los modelos Peewee y los scripts SQL.

## Entidades y relaciones

- **Proyecto** contiene tableros y tiene usuarios asociados mediante
  `ProyectoUsuario`, con rol.
- **Tablero** pertenece a un proyecto y puede tener usuarios con roles propios
  mediante `TableroUsuario`.
- **Lista** pertenece a un tablero y tiene una posición para ordenar el flujo.
- **Tarjeta** pertenece a una lista; puede incluir descripción, estado y fecha
  límite.
- **Usuario** puede tener asignaciones a tarjetas y escribir comentarios.
- **Etiqueta** puede asociarse a varias tarjetas mediante `TarjetaEtiqueta`.
- **Comentario** pertenece a una tarjeta y a un usuario.
- Las relaciones de pertenencia y asociación usan claves foráneas; muchas
  eliminaciones en cascada están definidas en el esquema.

## Comportamiento existente

- El menú de gestión permite registrar/autenticar usuarios y administrar
  proyectos, tableros, listas, tarjetas, miembros, comentarios, etiquetas y
  asignaciones.
- El menú de consultas permite listar usuarios, proyectos y miembros, explorar
  tableros/listas/tarjetas, filtrar tarjetas por estado y buscar usuarios por
  correo.
- Los roles disponibles son `Administrador`, `Lider`, `Miembro` y
  `Observador`. El acceso de un usuario a un tablero puede heredarse de su rol
  en el proyecto; un rol asignado directamente al tablero prevalece. Las
  operaciones de gestión requieren rol de Administrador o Lider; las
  operaciones de tarjetas permiten también Miembro, según la regla concreta.
- Los usuarios nuevos deben tener correo válido y contraseña de 8 a 128
  caracteres que contenga mayúscula, minúscula, número y símbolo, sin espacios.
  La contraseña se confirma antes del registro y se almacena como hash
  bcrypt con sal aleatoria (con prehash SHA-256 para no truncar contraseñas
  largas), nunca como texto plano. Los hashes PBKDF2 existentes se migran a
  bcrypt al iniciar sesión correctamente.
- El campo `Usuario.es_admin` define el rol administrativo global. Solo un
  administrador puede listar, crear, actualizar o eliminar cuentas desde el
  menú de gestión; el último administrador no se puede eliminar. Las
  operaciones de negocio también comprueban este permiso, no solo el menú.
- El primer administrador no se asigna automáticamente a la primera cuenta.
  El operador configura `admin_email` en `.env` y ejecuta
  `python main.py --bootstrap-admin`; el comando permite crear o restablecer
  únicamente esa cuenta y solo si todavía no existe un administrador.
- El menú de consultas es de solo lectura y actualmente no requiere iniciar
  sesión. Analiza los datos que expone antes de recomendar cambios de privacidad
  y no lo confundas con el menú de administración de cuentas.
- Las cuentas heredadas con `password_hash` nulo no pueden iniciar sesión ni
  establecer su propia contraseña. El administrador debe restablecerla; para
  recuperar el primer administrador se utiliza el comando de bootstrap local.

## Qué necesito de tu análisis

1. Recorre el código y confirma los problemas con referencias a archivos y
   líneas; no te limites a buscar palabras clave ni a inferir por nombres.
2. Prioriza errores funcionales reproducibles, inconsistencias de esquema,
   defectos en validación y permisos, y fallos de manejo de errores.
3. Distingue claramente entre errores, riesgos de seguridad y mejoras
   opcionales. Explica impacto y pasos para reproducir cada error.
4. Si propones cambios, que sean pequeños, compatibles con la arquitectura y
   con los flujos descritos. No elimines datos ni alteres credenciales.
5. Si tienes acceso al entorno, ejecuta las comprobaciones pertinentes y
   reporta exactamente cuáles pasaron o fallaron. No afirmes que ejecutaste
   pruebas que no hayas podido correr.
6. Antes de asumir un comportamiento distinto del documentado, explica la
   ambigüedad y solicita confirmación.
7. Termina con un resumen priorizado y una lista de pruebas recomendadas.

---
