"""Menú de consola para operar proyectos, tableros, listas y tarjetas."""
from peewee import PeeweeException

from presentacion.auxiliares import mostrar_tabla, nombre_app, version_app
from Datos.conexion import conectar_bd
from Datos.modelos import models as modelos
from Datos.modelos.models import (
    Comentario,
    Etiqueta,
    Lista,
    Proyecto,
    ProyectoUsuario,
    Tablero,
    Tarjeta,
    TarjetaEtiqueta,
    Usuario,
)
from Datos.repositorio import (
    repo_comentario,
    repo_etiqueta,
    repo_lista,
    repo_proyecto,
    repo_tablero,
    repo_tarjeta,
    repo_usuario,
)
from negocio import servicio_usuario
from negocio import servicio_trello as servicio


class SalirMenu(Exception):
    """Señala una solicitud para salir mediante Ctrl+C o Ctrl+D."""


def pedir(mensaje):
    try:
        return input(mensaje).strip()
    except (EOFError, KeyboardInterrupt) as error:
        raise SalirMenu from error


def pedir_entero(mensaje, opcional=False):
    while True:
        valor = pedir(mensaje)
        if opcional and not valor:
            return None
        try:
            numero = int(valor)
            if numero > 0:
                return numero
        except ValueError:
            pass
        print("Ingresa un número entero mayor que cero.")


def ejecutar_accion(accion, *args, **kwargs):
    try:
        resultado = accion(*args, **kwargs)
        return resultado
    except (ValueError, PermissionError) as error:
        print(f"No se pudo completar la operación: {error}")
    except PeeweeException as error:
        print(
            "Error de base de datos. Verifica que MySQL/XAMPP esté activo, "
            f"la conexión del .env y los datos relacionados: {error}"
        )
    return None


def _usuario_actual():
    while True:
        usuarios = list(repo_usuario.listado_usuarios())
        if usuarios:
            mostrar_tabla(
                "USUARIOS DISPONIBLES",
                ["ID", "Nombre", "Email"],
                [
                    [usuario.id_usuario, usuario.nombre, usuario.email]
                    for usuario in usuarios
                ],
                "No hay usuarios registrados.",
            )
            print("0. Registrar un usuario nuevo")
            seleccion = pedir("Selecciona el usuario de esta sesión: ")
            if seleccion.isdigit() and int(seleccion) > 0:
                usuario = repo_usuario.obtener_usuario_por_id(int(seleccion))
                if usuario:
                    return usuario
                print("No existe ese usuario.")
                continue
            if seleccion != "0":
                print("Selecciona un ID válido o 0 para registrar un usuario.")
                continue
        nombre = pedir("Nombre: ")
        email = pedir("Email: ")
        try:
            usuario = servicio_usuario.crear_usuario(nombre, email)
        except ValueError as error:
            print(f"No se pudo registrar el usuario: {error}")
            continue
        except PeeweeException as error:
            print(f"No se pudo registrar el usuario: {error}")
            continue
        print(f"Sesión iniciada como {usuario.nombre} (ID {usuario.id_usuario}).")
        return usuario


def listar_usuarios():
    usuarios = servicio_usuario.procesar_listado_usuario()
    mostrar_tabla(
        "USUARIOS",
        ["ID", "Nombre", "Email"],
        [
            [usuario.id_usuario, usuario.nombre, usuario.email]
            for usuario in usuarios
        ],
        "No hay usuarios registrados.",
    )


def menu_usuarios():
    while True:
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("1. Listar | 2. Crear | 3. Actualizar | 4. Eliminar | 0. Volver")
        opcion = pedir("Opción: ")
        if opcion == "0":
            return
        if opcion == "1":
            ejecutar_accion(listar_usuarios)
        elif opcion == "2":
            nombre = pedir("Nombre: ")
            email = pedir("Email: ")
            usuario = ejecutar_accion(
                servicio_usuario.crear_usuario, nombre, email
            )
            if usuario:
                print(f"Usuario registrado (ID {usuario.id_usuario}).")
        elif opcion == "3":
            usuario_id = pedir_entero("ID del usuario: ")
            nombre = pedir("Nuevo nombre (vacío para mantener): ") or None
            email = pedir("Nuevo email (vacío para mantener): ") or None
            if email and "@" not in email:
                print("El email no es válido.")
                continue
            usuario = ejecutar_accion(
                repo_usuario.actualizar_usuario, usuario_id, nombre, email
            )
            print("Usuario actualizado." if usuario else "Usuario no encontrado.")
        elif opcion == "4":
            usuario_id = pedir_entero("ID del usuario a eliminar: ")
            if pedir("La eliminación borra sus asignaciones. ¿Confirmar? (s/N): ").lower() == "s":
                eliminado = ejecutar_accion(repo_usuario.eliminar_usuario, usuario_id)
                print("Usuario eliminado." if eliminado else "Usuario no encontrado.")
        else:
            print("Opción no válida.")


def listar_proyectos():
    proyectos = repo_proyecto.listado_proyectos()
    mostrar_tabla(
        "PROYECTOS",
        ["ID", "Nombre", "Descripción"],
        [
            [
                proyecto.id_proyecto,
                proyecto.nombre_proyecto,
                proyecto.descripcion or "Sin descripción",
            ]
            for proyecto in proyectos
        ],
        "No hay proyectos registrados.",
    )


def _listar_miembros_proyecto(id_proyecto):
    asignaciones = repo_proyecto.listar_usuarios_proyecto(id_proyecto)
    filas = []
    for asignacion in asignaciones:
        usuario = Usuario.get_by_id(asignacion.id_usuario)
        filas.append([usuario.id_usuario, usuario.nombre, asignacion.rol])
    mostrar_tabla(
        "MIEMBROS DEL PROYECTO",
        ["ID usuario", "Nombre", "Rol"],
        filas,
        "El proyecto no tiene miembros.",
    )


def menu_proyectos(usuario_actual):
    while True:
        print("\n--- GESTIÓN DE PROYECTOS ---")
        print("1. Listar | 2. Crear | 3. Actualizar | 4. Eliminar")
        print("5. Asignar miembro/rol | 6. Quitar miembro | 0. Volver")
        opcion = pedir("Opción: ")
        if opcion == "0":
            return
        if opcion == "1":
            ejecutar_accion(listar_proyectos)
        elif opcion == "2":
            nombre = pedir("Nombre: ")
            descripcion = pedir("Descripción (opcional): ")
            proyecto = ejecutar_accion(
                servicio.crear_proyecto,
                nombre,
                descripcion,
                usuario_actual.id_usuario,
            )
            if proyecto:
                print(f"Proyecto creado (ID {proyecto.id_proyecto}).")
        elif opcion == "3":
            proyecto_id = pedir_entero("ID del proyecto: ")
            nombre = pedir("Nuevo nombre (vacío para mantener): ") or None
            descripcion = pedir("Nueva descripción (vacío para mantener): ") or None
            proyecto = ejecutar_accion(
                servicio.actualizar_proyecto,
                proyecto_id,
                usuario_actual.id_usuario,
                nombre,
                descripcion,
            )
            print("Proyecto actualizado." if proyecto else "Proyecto no encontrado.")
        elif opcion == "4":
            proyecto_id = pedir_entero("ID del proyecto: ")
            if pedir("Se borrarán también sus tableros y tarjetas. ¿Confirmar? (s/N): ").lower() == "s":
                eliminado = ejecutar_accion(
                    servicio.eliminar_proyecto, proyecto_id, usuario_actual.id_usuario
                )
                print("Proyecto eliminado." if eliminado else "Proyecto no encontrado.")
        elif opcion in ("5", "6"):
            proyecto_id = pedir_entero("ID del proyecto: ")
            if opcion == "5":
                usuario_id = pedir_entero("ID del usuario a asignar: ")
                rol = pedir("Rol (Administrador/Lider/Miembro/Observador): ")
                asignacion = ejecutar_accion(
                    servicio.asignar_usuario_proyecto,
                    proyecto_id,
                    usuario_id,
                    rol,
                    usuario_actual.id_usuario,
                )
                if asignacion:
                    print(f"Rol {asignacion.rol} asignado.")
            else:
                usuario_id = pedir_entero("ID del usuario a quitar: ")
                quitado = ejecutar_accion(
                    servicio.eliminar_usuario_proyecto,
                    proyecto_id,
                    usuario_id,
                    usuario_actual.id_usuario,
                )
                print("Miembro quitado." if quitado else "El usuario no estaba asignado.")
        else:
            print("Opción no válida.")


def crear_proyecto_consola(usuario_actual):
    nombre = pedir("Nombre del proyecto: ")
    descripcion = pedir("Descripción: ")
    if not nombre:
        print("El nombre del proyecto es obligatorio.")
        return
    proyecto = ejecutar_accion(
        servicio.crear_proyecto,
        nombre,
        descripcion,
        usuario_actual.id_usuario,
    )
    if proyecto:
        print("Proyecto creado.")


def _mostrar_tablero(id_tablero):
    listas = repo_lista.listado_listas_por_tablero(id_tablero)
    filas = []
    for lista in listas:
        tarjetas = list(repo_tarjeta.listado_tarjetas_por_lista(lista.id_lista))
        if not tarjetas:
            filas.append(
                [
                    lista.id_lista,
                    lista.nombre_lista,
                    lista.posicion,
                    "-",
                    "Sin tarjetas",
                    "-",
                    "-",
                    "-",
                    "-",
                ]
            )
        for tarjeta in tarjetas:
            asignados = [
                Usuario.get_by_id(asignacion.id_usuario).nombre
                for asignacion in repo_tarjeta.listar_usuarios_asignados(
                    tarjeta.id_tarjeta
                )
            ]
            etiquetas = (
                Etiqueta.select()
                .join(TarjetaEtiqueta)
                .where(TarjetaEtiqueta.id_tarjeta == tarjeta.id_tarjeta)
                .order_by(Etiqueta.nombre)
            )
            nombres_etiquetas = [etiqueta.nombre for etiqueta in etiquetas]
            comentarios = repo_comentario.listado_comentarios_por_tarjeta(
                tarjeta.id_tarjeta
            )
            comentarios_texto = []
            for comentario in comentarios:
                autor = Usuario.get_by_id(comentario.id_usuario)
                comentarios_texto.append(f"{autor.nombre}: {comentario.texto}")
            filas.append(
                [
                    lista.id_lista,
                    lista.nombre_lista,
                    lista.posicion,
                    tarjeta.id_tarjeta,
                    tarjeta.titulo,
                    tarjeta.estado or "Pendiente",
                    ", ".join(asignados) or "-",
                    ", ".join(nombres_etiquetas) or "-",
                    "\n".join(comentarios_texto) or "-",
                ]
            )
    if not listas:
        filas = []
    mostrar_tabla(
        "CONTENIDO DEL TABLERO",
        [
            "ID lista",
            "Lista",
            "Posición",
            "ID tarjeta",
            "Tarjeta",
            "Estado",
            "Asignados",
            "Etiquetas",
            "Comentarios",
        ],
        filas,
        "Este tablero todavía no tiene listas.",
    )


def _seleccionar_tarjeta(id_tablero):
    filas = []
    for lista in repo_lista.listado_listas_por_tablero(id_tablero):
        for tarjeta in repo_tarjeta.listado_tarjetas_por_lista(lista.id_lista):
            filas.append([tarjeta.id_tarjeta, tarjeta.titulo, lista.nombre_lista])
    mostrar_tabla(
        "TARJETAS",
        ["ID", "Título", "Lista"],
        filas,
        "No hay tarjetas en este tablero.",
    )
    return pedir_entero("ID de la tarjeta: ")


def _gestionar_miembros_tablero(id_tablero, usuario_actual):
    filas = []
    for asignacion in repo_tablero.listar_usuarios_tablero(id_tablero):
        usuario = Usuario.get_by_id(asignacion.id_usuario)
        filas.append([usuario.id_usuario, usuario.nombre, asignacion.rol])
    mostrar_tabla(
        "MIEMBROS DEL TABLERO",
        ["ID usuario", "Nombre", "Rol"],
        filas,
        "El tablero no tiene miembros.",
    )
    opcion = pedir("1. Asignar/cambiar rol | 2. Quitar miembro | 0. Volver: ")
    if opcion == "1":
        usuario_id = pedir_entero("ID del usuario: ")
        rol = pedir("Rol (Administrador/Lider/Miembro/Observador): ")
        asignacion = ejecutar_accion(
            servicio.asignar_usuario_tablero,
            id_tablero,
            usuario_id,
            rol,
            usuario_actual.id_usuario,
        )
        if asignacion:
            print(f"Rol {asignacion.rol} asignado.")
    elif opcion == "2":
        usuario_id = pedir_entero("ID del usuario: ")
        quitado = ejecutar_accion(
            servicio.eliminar_usuario_tablero,
            id_tablero,
            usuario_id,
            usuario_actual.id_usuario,
        )
        print("Miembro quitado." if quitado else "El usuario no estaba asignado.")


def menu_tablero(tablero, usuario_actual):
    while True:
        rol = ejecutar_accion(
            servicio.obtener_rol_tablero, tablero.id_tablero, usuario_actual.id_usuario
        )
        if not rol:
            return
        print(f"\n--- TABLERO {tablero.titulo} | Rol: {rol} ---")
        print("1. Ver | 2. Crear lista | 3. Actualizar lista | 4. Eliminar lista")
        print("5. Crear tarjeta | 6. Actualizar tarjeta | 7. Eliminar tarjeta")
        print("8. Gestionar miembros | 9. Comentar | 10. Eliminar comentario")
        print("11. Crear etiqueta | 12. Asignar etiqueta | 13. Quitar etiqueta")
        print("14. Actualizar tablero | 15. Eliminar tablero | 0. Volver")
        print("16. Asignar usuario a tarjeta | 17. Quitar asignación")
        print("18. Actualizar comentario | 19. Actualizar etiqueta | 20. Eliminar etiqueta")
        opcion = pedir("Opción: ")
        if opcion == "0":
            return
        if opcion == "1":
            ejecutar_accion(_mostrar_tablero, tablero.id_tablero)
        elif opcion == "2":
            nombre = pedir("Nombre de la lista: ")
            posicion = pedir("Posición (entero, predeterminado 0): ") or "0"
            lista = ejecutar_accion(
                servicio.crear_lista,
                tablero.id_tablero,
                nombre,
                usuario_actual.id_usuario,
                posicion,
            )
            if lista:
                print(f"Lista creada (ID {lista.id_lista}).")
        elif opcion == "3":
            lista_id = pedir_entero("ID de la lista: ")
            nombre = pedir("Nuevo nombre (vacío para mantener): ") or None
            posicion = pedir("Nueva posición (vacío para mantener): ")
            lista = ejecutar_accion(
                servicio.actualizar_lista,
                lista_id,
                usuario_actual.id_usuario,
                nombre,
                posicion or None,
            )
            print("Lista actualizada." if lista else "Lista no encontrada.")
        elif opcion == "4":
            lista_id = pedir_entero("ID de la lista: ")
            if pedir("Se eliminarán también sus tarjetas. ¿Confirmar? (s/N): ").lower() == "s":
                eliminado = ejecutar_accion(
                    servicio.eliminar_lista, lista_id, usuario_actual.id_usuario
                )
                print("Lista eliminada." if eliminado else "Lista no encontrada.")
        elif opcion == "5":
            lista_id = pedir_entero("ID de la lista: ")
            titulo = pedir("Título: ")
            descripcion = pedir("Descripción (opcional): ")
            estado = pedir("Estado (predeterminado Pendiente): ") or "Pendiente"
            fecha = pedir("Fecha límite AAAA-MM-DD (opcional): ")
            tarjeta = ejecutar_accion(
                servicio.crear_tarjeta,
                lista_id,
                titulo,
                descripcion,
                estado,
                fecha,
                usuario_actual.id_usuario,
            )
            if tarjeta:
                print(f"Tarjeta creada (ID {tarjeta.id_tarjeta}).")
        elif opcion == "6":
            tarjeta_id = _seleccionar_tarjeta(tablero.id_tablero)
            titulo = pedir("Nuevo título (vacío para mantener): ") or None
            descripcion = pedir("Nueva descripción (vacío para mantener): ") or None
            estado = pedir("Nuevo estado (vacío para mantener): ") or None
            fecha = pedir("Nueva fecha AAAA-MM-DD (vacío para mantener): ") or None
            tarjeta = ejecutar_accion(
                servicio.actualizar_tarjeta,
                tarjeta_id,
                usuario_actual.id_usuario,
                titulo,
                descripcion,
                estado,
                fecha,
            )
            print("Tarjeta actualizada." if tarjeta else "Tarjeta no encontrada.")
        elif opcion == "7":
            tarjeta_id = _seleccionar_tarjeta(tablero.id_tablero)
            if pedir("¿Eliminar la tarjeta y sus comentarios? (s/N): ").lower() == "s":
                eliminado = ejecutar_accion(
                    servicio.eliminar_tarjeta, tarjeta_id, usuario_actual.id_usuario
                )
                print("Tarjeta eliminada." if eliminado else "Tarjeta no encontrada.")
        elif opcion == "8":
            ejecutar_accion(
                _gestionar_miembros_tablero,
                tablero.id_tablero,
                usuario_actual,
            )
        elif opcion == "9":
            tarjeta_id = _seleccionar_tarjeta(tablero.id_tablero)
            texto = pedir("Comentario: ")
            comentario = ejecutar_accion(
                servicio.crear_comentario,
                tarjeta_id,
                usuario_actual.id_usuario,
                texto,
            )
            if comentario:
                print("Comentario agregado.")
        elif opcion == "10":
            tarjeta_id = _seleccionar_tarjeta(tablero.id_tablero)
            comentarios = repo_comentario.listado_comentarios_por_tarjeta(tarjeta_id)
            mostrar_tabla(
                "COMENTARIOS DE LA TARJETA",
                ["ID", "Comentario", "Autor", "Fecha"],
                [
                    [
                        comentario.id_comentario,
                        comentario.texto,
                        Usuario.get_by_id(comentario.id_usuario).nombre,
                        comentario.fecha_creacion,
                    ]
                    for comentario in comentarios
                ],
                "La tarjeta no tiene comentarios.",
            )
            comentario_id = pedir_entero("ID del comentario a eliminar: ")
            eliminado = ejecutar_accion(
                servicio.eliminar_comentario,
                comentario_id,
                usuario_actual.id_usuario,
            )
            print("Comentario eliminado." if eliminado else "Comentario no encontrado.")
        elif opcion == "11":
            nombre, color = pedir("Nombre de la etiqueta: "), pedir("Color (ej. #ff0000): ")
            etiqueta = ejecutar_accion(
                servicio.crear_etiqueta,
                nombre,
                color,
                tablero.id_tablero,
                usuario_actual.id_usuario,
            )
            if etiqueta:
                print(f"Etiqueta creada (ID {etiqueta.id_etiqueta}).")
        elif opcion in ("12", "13"):
            tarjeta_id = _seleccionar_tarjeta(tablero.id_tablero)
            etiquetas = repo_etiqueta.listado_etiquetas()
            mostrar_tabla(
                "ETIQUETAS",
                ["ID", "Nombre", "Color"],
                [
                    [etiqueta.id_etiqueta, etiqueta.nombre, etiqueta.color]
                    for etiqueta in etiquetas
                ],
                "No hay etiquetas registradas.",
            )
            etiqueta_id = pedir_entero("ID de la etiqueta: ")
            if opcion == "12":
                relacion = ejecutar_accion(
                    servicio.asignar_etiqueta,
                    tarjeta_id,
                    etiqueta_id,
                    usuario_actual.id_usuario,
                )
                if relacion:
                    print("Etiqueta asignada.")
            else:
                eliminado = ejecutar_accion(
                    servicio.eliminar_etiqueta_tarjeta,
                    tarjeta_id,
                    etiqueta_id,
                    usuario_actual.id_usuario,
                )
                print("Etiqueta retirada." if eliminado else "No estaba asignada.")
        elif opcion == "14":
            titulo = pedir("Nuevo título: ")
            actualizado = ejecutar_accion(
                servicio.actualizar_tablero,
                tablero.id_tablero,
                usuario_actual.id_usuario,
                titulo,
            )
            if actualizado:
                print("Tablero actualizado.")
        elif opcion == "15":
            if pedir("¿Eliminar el tablero y todo su contenido? (s/N): ").lower() == "s":
                eliminado = ejecutar_accion(
                    servicio.eliminar_tablero,
                    tablero.id_tablero,
                    usuario_actual.id_usuario,
                )
                if eliminado:
                    print("Tablero eliminado.")
                    return
        elif opcion in ("16", "17"):
            tarjeta_id = _seleccionar_tarjeta(tablero.id_tablero)
            if opcion == "16":
                mostrar_tabla(
                    "USUARIOS REGISTRADOS",
                    ["ID", "Nombre", "Email"],
                    [
                        [usuario.id_usuario, usuario.nombre, usuario.email]
                        for usuario in repo_usuario.listado_usuarios()
                    ],
                    "No hay usuarios registrados.",
                )
                usuario_id = pedir_entero("ID del miembro a asignar: ")
                asignacion = ejecutar_accion(
                    servicio.asignar_usuario_tarjeta,
                    tarjeta_id,
                    usuario_id,
                    usuario_actual.id_usuario,
                )
                if asignacion:
                    print("Usuario asignado a la tarjeta.")
            else:
                asignaciones = repo_tarjeta.listar_usuarios_asignados(tarjeta_id)
                usuarios_asignados = []
                for asignacion in asignaciones:
                    usuario = Usuario.get_by_id(asignacion.id_usuario)
                    usuarios_asignados.append([usuario.id_usuario, usuario.nombre])
                mostrar_tabla(
                    "USUARIOS ASIGNADOS A LA TARJETA",
                    ["ID", "Nombre"],
                    usuarios_asignados,
                    "La tarjeta no tiene usuarios asignados.",
                )
                usuario_id = pedir_entero("ID del usuario a quitar: ")
                eliminado = ejecutar_accion(
                    servicio.quitar_usuario_tarjeta,
                    tarjeta_id,
                    usuario_id,
                    usuario_actual.id_usuario,
                )
                print("Asignación retirada." if eliminado else "No estaba asignado.")
        elif opcion == "18":
            tarjeta_id = _seleccionar_tarjeta(tablero.id_tablero)
            comentarios = repo_comentario.listado_comentarios_por_tarjeta(tarjeta_id)
            mostrar_tabla(
                "COMENTARIOS DE LA TARJETA",
                ["ID", "Comentario", "Autor", "Fecha"],
                [
                    [
                        comentario.id_comentario,
                        comentario.texto,
                        Usuario.get_by_id(comentario.id_usuario).nombre,
                        comentario.fecha_creacion,
                    ]
                    for comentario in comentarios
                ],
                "La tarjeta no tiene comentarios.",
            )
            comentario_id = pedir_entero("ID del comentario a actualizar: ")
            texto = pedir("Nuevo comentario: ")
            comentario = ejecutar_accion(
                servicio.actualizar_comentario,
                comentario_id,
                usuario_actual.id_usuario,
                texto,
            )
            print("Comentario actualizado." if comentario else "Comentario no encontrado.")
        elif opcion in ("19", "20"):
            etiquetas = repo_etiqueta.listado_etiquetas()
            mostrar_tabla(
                "ETIQUETAS",
                ["ID", "Nombre", "Color"],
                [
                    [etiqueta.id_etiqueta, etiqueta.nombre, etiqueta.color]
                    for etiqueta in etiquetas
                ],
                "No hay etiquetas registradas.",
            )
            etiqueta_id = pedir_entero("ID de la etiqueta: ")
            if opcion == "19":
                nombre = pedir("Nuevo nombre: ")
                color = pedir("Nuevo color: ")
                etiqueta = ejecutar_accion(
                    servicio.actualizar_etiqueta,
                    etiqueta_id,
                    nombre,
                    color,
                    tablero.id_tablero,
                    usuario_actual.id_usuario,
                )
                print("Etiqueta actualizada." if etiqueta else "Etiqueta no encontrada.")
            elif pedir("Eliminar etiqueta de todas las tarjetas. ¿Confirmar? (s/N): ").lower() == "s":
                eliminado = ejecutar_accion(
                    servicio.eliminar_etiqueta,
                    etiqueta_id,
                    tablero.id_tablero,
                    usuario_actual.id_usuario,
                )
                print("Etiqueta eliminada." if eliminado else "Etiqueta no encontrada.")
        else:
            print("Opción no válida.")


def menu_tableros(usuario_actual):
    while True:
        print("\n--- TABLEROS ---")
        tableros = ejecutar_accion(
            servicio.listar_tableros_usuario, usuario_actual.id_usuario
        )
        if tableros is None:
            return
        filas = []
        for tablero in tableros:
            proyecto = Proyecto.get_by_id(tablero.id_proyecto)
            rol = servicio.rol_en_tablero(tablero.id_tablero, usuario_actual.id_usuario)
            filas.append(
                [
                    tablero.id_tablero,
                    tablero.titulo,
                    proyecto.nombre_proyecto,
                    rol,
                ]
            )
        mostrar_tabla(
            "TABLEROS",
            ["ID", "Tablero", "Proyecto", "Rol"],
            filas,
            "No tienes tableros disponibles.",
        )
        print("1. Crear tablero | 2. Abrir tablero | 0. Volver")
        opcion = pedir("Opción: ")
        if opcion == "0":
            return
        if opcion == "1":
            listar_proyectos()
            proyecto_id = pedir_entero("ID del proyecto: ")
            titulo = pedir("Título del tablero: ")
            tablero = ejecutar_accion(
                servicio.crear_tablero,
                proyecto_id,
                titulo,
                usuario_actual.id_usuario,
            )
            if tablero:
                print(f"Tablero creado (ID {tablero.id_tablero}).")
        elif opcion == "2":
            tablero_id = pedir_entero("ID del tablero a abrir: ")
            tablero = repo_tablero.obtener_tablero_por_id(tablero_id)
            if not tablero:
                print("No existe ese tablero.")
                continue
            if servicio.rol_en_tablero(tablero_id, usuario_actual.id_usuario) is None:
                print("No tienes acceso a ese tablero.")
                continue
            menu_tablero(tablero, usuario_actual)
        else:
            print("Opción no válida.")


def cargar_menu():
    if not conectar_bd() or not modelos.crear_tablas():
        return
    try:
        usuario_actual = _usuario_actual()
        while True:
            print(f"\n{nombre_app} v{version_app} — sesión: {usuario_actual.nombre}")
            print("1. Crear proyecto | 2. Listar proyectos | 3. Tableros")
            print("4. Cambiar usuario | 5. Gestionar usuarios")
            print("6. Gestionar proyectos | 0. Salir")
            opcion = pedir("Opción: ")
            if opcion == "0":
                print("Hasta luego.")
                return
            if opcion == "1":
                crear_proyecto_consola(usuario_actual)
            elif opcion == "2":
                ejecutar_accion(listar_proyectos)
            elif opcion == "3":
                menu_tableros(usuario_actual)
            elif opcion == "4":
                usuario_actual = _usuario_actual()
            elif opcion == "5":
                menu_usuarios()
            elif opcion == "6":
                menu_proyectos(usuario_actual)
            else:
                print("Opción no válida.")
    except SalirMenu:
        print("\nSesión finalizada.")
    except PeeweeException as error:
        print(f"Error de base de datos: {error}")


if __name__ == "__main__":
    cargar_menu()
