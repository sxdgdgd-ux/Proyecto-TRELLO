"""Menú interactivo para consultar los datos del tablero."""
from Datos.modelos.models import (
    AsignacionTarjeta,
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
from Datos.conexion import conectar_bd
from Datos.modelos import models as modelos
from Datos.repositorio import repo_usuario
from presentacion.auxiliares import mostrar_tabla as _mostrar_tabla


def mostrar_menu():
    print("\n==================================================")
    print("       MENU DE CONSULTAS INTERACTIVAS")
    print("==================================================")
    print("1. Consultar todos los Usuarios")
    print("2. Consultar todos los Proyectos y sus Miembros")
    print("3. Consultar Tableros y sus Listas")
    print("4. Consultar Tarjetas por Estado")
    print("5. Buscar Usuario por Email")
    print("0. Salir")
    print("==================================================")


def listar_usuarios():
    usuarios = repo_usuario.listado_usuarios()
    _mostrar_tabla(
        "LISTA DE USUARIOS",
        ["ID", "Nombre", "Email"],
        [[u.id_usuario, u.nombre, u.email] for u in usuarios],
        "No hay usuarios registrados.",
    )


def listar_proyectos():
    proyectos = Proyecto.select().order_by(Proyecto.id_proyecto)
    if not proyectos:
        _mostrar_tabla(
            "PROYECTOS Y MIEMBROS",
            ["ID proyecto", "Proyecto", "Descripción", "Miembro", "Rol"],
            [],
            "No hay proyectos registrados.",
        )
        return

    filas = []
    for p in proyectos:
        miembros = (
            ProyectoUsuario.select(ProyectoUsuario, Usuario)
            .join(Usuario)
            .where(ProyectoUsuario.id_proyecto == p.id_proyecto)
            .order_by(Usuario.nombre, Usuario.id_usuario)
        )
        miembros = list(miembros)
        if miembros:
            filas.extend(
                [
                    p.id_proyecto,
                    p.nombre_proyecto,
                    p.descripcion or "Sin descripción",
                    miembro.id_usuario.nombre,
                    miembro.rol,
                ]
                for miembro in miembros
            )
        else:
            filas.append(
                [
                    p.id_proyecto,
                    p.nombre_proyecto,
                    p.descripcion or "Sin descripción",
                    "Sin miembros",
                    "-",
                ]
            )
    _mostrar_tabla(
        "PROYECTOS Y MIEMBROS",
        ["ID proyecto", "Proyecto", "Descripción", "Miembro", "Rol"],
        filas,
        "No hay proyectos registrados.",
    )


def listar_tableros():
    tableros = Tablero.select().order_by(Tablero.id_proyecto, Tablero.id_tablero)
    if not tableros:
        _mostrar_tabla(
            "TABLEROS, LISTAS Y TARJETAS",
            [
                "ID tablero",
                "Tablero",
                "Proyecto",
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
            [],
            "No hay tableros registrados.",
        )
        return

    filas = []
    for t in tableros:
        listas = (
            Lista.select()
            .where(Lista.id_tablero == t.id_tablero)
            .order_by(Lista.posicion, Lista.id_lista)
        )
        listas = list(listas)
        if not listas:
            filas.append(
                [
                    t.id_tablero,
                    t.titulo,
                    t.id_proyecto.nombre_proyecto,
                    "-",
                    "Sin listas",
                    "-",
                    "-",
                    "-",
                    "-",
                    "-",
                    "-",
                    "-",
                ]
            )
        for l in listas:
            tarjetas = (
                Tarjeta.select()
                .where(Tarjeta.id_lista == l.id_lista)
                .order_by(Tarjeta.id_tarjeta)
            )
            tarjetas = list(tarjetas)
            if not tarjetas:
                filas.append(
                    [
                        t.id_tablero,
                        t.titulo,
                        t.id_proyecto.nombre_proyecto,
                        l.id_lista,
                        l.nombre_lista,
                        l.posicion,
                        "-",
                        "Sin tarjetas",
                        "-",
                        "-",
                        "-",
                        "-",
                    ]
                )
            for tarjeta in tarjetas:
                asignaciones = (
                    AsignacionTarjeta.select(AsignacionTarjeta, Usuario)
                    .join(Usuario)
                    .where(AsignacionTarjeta.id_tarjeta == tarjeta.id_tarjeta)
                    .order_by(Usuario.nombre, Usuario.id_usuario)
                )
                nombres = [
                    asignacion.id_usuario.nombre for asignacion in asignaciones
                ]
                etiquetas = (
                    TarjetaEtiqueta.select(TarjetaEtiqueta, Etiqueta)
                    .join(Etiqueta)
                    .where(TarjetaEtiqueta.id_tarjeta == tarjeta.id_tarjeta)
                    .order_by(Etiqueta.nombre)
                )
                etiquetas_nombres = [
                    relacion.id_etiqueta.nombre for relacion in etiquetas
                ]
                comentarios = (
                    Comentario.select(Comentario, Usuario)
                    .join(Usuario)
                    .where(Comentario.id_tarjeta == tarjeta.id_tarjeta)
                    .order_by(Comentario.fecha_creacion, Comentario.id_comentario)
                )
                comentarios_texto = [
                    f"{comentario.id_usuario.nombre}: {comentario.texto}"
                    for comentario in comentarios
                ]
                filas.append(
                    [
                        t.id_tablero,
                        t.titulo,
                        t.id_proyecto.nombre_proyecto,
                        l.id_lista,
                        l.nombre_lista,
                        l.posicion,
                        tarjeta.id_tarjeta,
                        tarjeta.titulo,
                        tarjeta.estado or "Sin estado",
                        ", ".join(nombres) or "-",
                        ", ".join(etiquetas_nombres) or "-",
                        "\n".join(comentarios_texto) or "-",
                    ]
                )
    _mostrar_tabla(
        "TABLEROS, LISTAS Y TARJETAS",
        [
            "ID tablero",
            "Tablero",
            "Proyecto",
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
        "No hay tableros registrados.",
    )


def listar_tarjetas_por_estado():
    print("\n--- FILTRAR TARJETAS ---")
    estado = input("Ingresa el estado a buscar (ej: Pendiente, En Progreso, Completado): ").strip()
    if not estado:
        print("Debes escribir un estado para realizar la búsqueda.")
        return
    tarjetas = (
        Tarjeta.select()
        .where(Tarjeta.estado.contains(estado))
        .order_by(Tarjeta.estado, Tarjeta.id_tarjeta)
    )
    if not tarjetas:
        _mostrar_tabla(
            "TARJETAS ENCONTRADAS",
            ["ID", "Título", "Estado", "Fecha límite"],
            [],
            f"No se encontraron tarjetas con el estado '{estado}'.",
        )
        return
    filas = [
        [tar.id_tarjeta, tar.titulo, tar.estado, tar.fecha_limite or "-"]
        for tar in tarjetas
    ]
    _mostrar_tabla(
        "TARJETAS ENCONTRADAS",
        ["ID", "Título", "Estado", "Fecha límite"],
        filas,
        f"No se encontraron tarjetas con el estado '{estado}'.",
    )


def buscar_usuario():
    email = input("\nIngresa el email a buscar: ").strip()
    usuario = Usuario.get_or_none(Usuario.email == email)
    if usuario:
        _mostrar_tabla(
            "USUARIO ENCONTRADO",
            ["ID", "Nombre", "Email"],
            [[usuario.id_usuario, usuario.nombre, usuario.email]],
            "No se encontró el usuario.",
        )
    else:
        _mostrar_tabla(
            "USUARIO ENCONTRADO",
            ["ID", "Nombre", "Email"],
            [],
            f"No existe ningún usuario registrado con el correo: {email}",
        )


def ejecutar():
    if not conectar_bd() or not modelos.crear_tablas():
        return
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (0-5): ").strip()

        if opcion == "1":
            listar_usuarios()
        elif opcion == "2":
            listar_proyectos()
        elif opcion == "3":
            listar_tableros()
        elif opcion == "4":
            listar_tarjetas_por_estado()
        elif opcion == "5":
            buscar_usuario()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")


if __name__ == '__main__':
    ejecutar()