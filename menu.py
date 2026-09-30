
# menu.py
from auxiliares import nombre_app, version_app
from models import (
    database, crear_tablas, Proyecto, Usuario, Tablero,
    Lista, Tarjeta
)


def cargar_menu():
    crear_tablas()
    while True:
        print(f"\n{nombre_app} v{version_app}")
        print("1. Crear proyecto")
        print("2. Listar proyectos")
        print("0. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            nombre = input("Nombre del proyecto: ")
            descripcion = input("Descripción: ")
            Proyecto.create(nombre_proyecto=nombre, descripcion=descripcion)
            print("Proyecto creado.")
        elif opcion == "2":
            for p in Proyecto.select():
                print(p.id_proyecto, p.nombre_proyecto)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")