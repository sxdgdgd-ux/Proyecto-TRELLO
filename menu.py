"""Menú básico para crear y consultar proyectos."""
from auxiliares import nombre_app, version_app
from models import Proyecto, crear_tablas


def cargar_menu():
    crear_tablas()
    while True:
        print(f"\n{nombre_app} v{version_app}")
        print("1. Crear proyecto")
        print("2. Listar proyectos")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del proyecto: ").strip()
            descripcion = input("Descripción: ").strip()
            if not nombre:
                print("El nombre del proyecto es obligatorio.")
                continue
            Proyecto.create(
                nombre_proyecto=nombre,
                descripcion=descripcion or None,
            )
            print("Proyecto creado.")
        elif opcion == "2":
            proyectos = Proyecto.select().order_by(Proyecto.id_proyecto)
            if not proyectos:
                print("No hay proyectos registrados.")
            for proyecto in proyectos:
                print(proyecto.id_proyecto, proyecto.nombre_proyecto)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    cargar_menu()
