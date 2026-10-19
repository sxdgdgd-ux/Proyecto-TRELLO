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
from conexion import conectar_bd


def mostrar_menu():
    print("\n==================================================")
    print("       📋 MENÚ DE CONSULTAS INTERACTIVAS")
    print("==================================================")
    print("1. Consultar todos los Usuarios")
    print("2. Consultar todos los Proyectos y sus Miembros")
    print("3. Consultar Tableros y sus Listas")
    print("4. Consultar Tarjetas por Estado")
    print("5. Buscar Usuario por Email")
    print("0. Salir")
    print("==================================================")


def listar_usuarios():
    print("\n--- LISTA DE USUARIOS ---")
    usuarios = Usuario.select().order_by(Usuario.nombre, Usuario.id_usuario)
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for u in usuarios:
        print(f"ID: {u.id_usuario} | Nombre: {u.nombre} | Email: {u.email}")


def listar_proyectos():
    print("\n--- PROYECTOS Y MIEMBROS ---")
    proyectos = Proyecto.select().order_by(Proyecto.id_proyecto)
    if not proyectos:
        print("No hay proyectos registrados.")
        return
    for p in proyectos:
        print(f"\n📌 Proyecto ID {p.id_proyecto}: {p.nombre_proyecto}")
        print(f"   Descripción: {p.descripcion}")
        
        miembros = (
            ProyectoUsuario.select(ProyectoUsuario, Usuario)
            .join(Usuario)
            .where(ProyectoUsuario.id_proyecto == p.id_proyecto)
            .order_by(Usuario.nombre, Usuario.id_usuario)
        )
        print("   Miembros:")
        for m in miembros:
            print(f"     - {m.id_usuario.nombre} (Rol: {m.rol})")


def listar_tableros():
    print("\n--- TABLEROS Y LISTAS ---")
    tableros = Tablero.select().order_by(Tablero.id_proyecto, Tablero.id_tablero)
    if not tableros:
        print("No hay tableros registrados.")
        return
    for t in tableros:
        print(f"\n📋 Tablero ID {t.id_tablero}: '{t.titulo}' (Proyecto: {t.id_proyecto.nombre_proyecto})")
        listas = (
            Lista.select()
            .where(Lista.id_tablero == t.id_tablero)
            .order_by(Lista.posicion, Lista.id_lista)
        )
        if not listas:
            print("   (Sin listas)")
        for l in listas:
            print(f"   📂 Lista ID {l.id_lista}: {l.nombre_lista} (Posición {l.posicion})")
            tarjetas = (
                Tarjeta.select()
                .where(Tarjeta.id_lista == l.id_lista)
                .order_by(Tarjeta.id_tarjeta)
            )
            if not tarjetas:
                print("      (Sin tarjetas)")
            for tarjeta in tarjetas:
                print(f"      🎴 {tarjeta.titulo} | Estado: {tarjeta.estado or 'Sin estado'}")
                asignaciones = (
                    AsignacionTarjeta.select(AsignacionTarjeta, Usuario)
                    .join(Usuario)
                    .where(AsignacionTarjeta.id_tarjeta == tarjeta.id_tarjeta)
                    .order_by(Usuario.nombre, Usuario.id_usuario)
                )
                if asignaciones:
                    nombres = [asignacion.id_usuario.nombre for asignacion in asignaciones]
                    print(f"         Asignado a: {', '.join(nombres)}")
                etiquetas = (
                    TarjetaEtiqueta.select(TarjetaEtiqueta, Etiqueta)
                    .join(Etiqueta)
                    .where(TarjetaEtiqueta.id_tarjeta == tarjeta.id_tarjeta)
                    .order_by(Etiqueta.nombre)
                )
                if etiquetas:
                    nombres = [relacion.id_etiqueta.nombre for relacion in etiquetas]
                    print(f"         Etiquetas: {', '.join(nombres)}")
                comentarios = (
                    Comentario.select(Comentario, Usuario)
                    .join(Usuario)
                    .where(Comentario.id_tarjeta == tarjeta.id_tarjeta)
                    .order_by(Comentario.fecha_creacion, Comentario.id_comentario)
                )
                for comentario in comentarios:
                    print(
                        f"         Comentario ({comentario.id_usuario.nombre}): "
                        f"{comentario.texto}"
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
        print(f"No se encontraron tarjetas con el estado '{estado}'.")
        return
    for tar in tarjetas:
        print(f"🎴 ID: {tar.id_tarjeta} | Título: '{tar.titulo}' | Estado: {tar.estado}")


def buscar_usuario():
    email = input("\nIngresa el email a buscar: ").strip()
    usuario = Usuario.get_or_none(Usuario.email == email)
    if usuario:
        print(f"\n✓ Usuario encontrado -> ID: {usuario.id_usuario} | Nombre: {usuario.nombre} | Email: {usuario.email}")
    else:
        print(f"\n❌ No existe ningún usuario registrado con el correo: {email}")


def ejecutar():
    if not conectar_bd():
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