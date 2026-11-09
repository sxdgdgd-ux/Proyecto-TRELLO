"""Punto de entrada principal del Gestor de Proyectos Trello."""

import sys

from presentacion.consultas import ejecutar as ejecutar_consultas
from presentacion.menu import cargar_menu, configurar_administrador_inicial


def main():
    """Permite elegir entre el menú de gestión y el de consultas."""
    if sys.argv[1:] == ["--bootstrap-admin"]:
        configurar_administrador_inicial()
        return

    while True:
        print("\n--- GESTOR DE PROYECTOS TRELLO ---")
        print("1. Gestión de usuarios, proyectos y tableros")
        print("2. Consultas")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            cargar_menu()
        elif opcion == "2":
            ejecutar_consultas()
        elif opcion == "0":
            print("Hasta luego.")
            return
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
