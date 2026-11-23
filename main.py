"""Punto de entrada principal del Gestor de Proyectos Trello."""

import sys

from presentacion.menu import cargar_menu, configurar_administrador_inicial


def main():
    """Inicia la aplicación; el menú solicita autenticación antes de entrar."""
    if sys.argv[1:] == ["--bootstrap-admin"]:
        configurar_administrador_inicial()
        return
    cargar_menu()


if __name__ == "__main__":
    main()
