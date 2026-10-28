"""Datos de presentación de la aplicación."""

from prettytable import PrettyTable

nombre_app = "Gestor de Proyectos Trello"
version_app = "1.0"


def mostrar_tabla(titulo, encabezados, filas, mensaje_vacio):
    """Imprime filas tabulares o un mensaje cuando no hay resultados."""
    print(f"\n--- {titulo} ---")
    if not filas:
        print(mensaje_vacio)
        return

    tabla = PrettyTable()
    tabla.field_names = encabezados
    tabla.add_rows(filas)
    print(tabla)
