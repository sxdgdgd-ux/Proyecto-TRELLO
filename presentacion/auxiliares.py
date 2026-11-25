"""Datos de presentación de la aplicación."""

from prettytable import PrettyTable
from auxiliares.configuracion import NOMBRE_APP, VERSION_APP

nombre_app = NOMBRE_APP
version_app = VERSION_APP


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
