"""Módulo principal para pruebas de integración de la base de datos y repositorios."""
from Datos.modelos.models import crear_tablas
from Datos.modelos.repositorio import repo_usuario, repo_proyecto, repo_tablero, repo_lista


def probar_sistema():
    """Ejecuta una prueba completa de flujo de datos."""
    print("=== 1. Creando tablas en MySQL ===")
    crear_tablas()
    print("✓ Tablas listadas/creadas correctamente.\n")

    print("=== 2. Probando Repositorio de Usuario ===")
    usuario = repo_usuario.crear_usuario(
        nombre="Alejandro Ortiz",
        email="alejandro@ejemplo.com"
    )
    print(f"✓ Usuario creado -> ID: {usuario.id_usuario}, Nombre: {usuario.nombre}")

    usuarios = repo_usuario.listado_usuarios()
    print(f" Total usuarios en BD: {len(usuarios)}\n")

    print("=== 3. Probando Repositorio de Proyecto ===")
    proyecto = repo_proyecto.crear_proyecto(
        nombre_proyecto="Proyecto Trello Modular",
        descripcion="Sistema de gestión de tareas con Peewee y MySQL"
    )
    print(f"✓ Proyecto creado -> ID: {proyecto.id_proyecto}, Nombre: {proyecto.nombre_proyecto}")

    repo_proyecto.asignar_usuario_a_proyecto(
        id_proyecto=proyecto.id_proyecto,
        id_usuario=usuario.id_usuario,
        rol="Administrador"
    )
    print(f"✓ Usuario {usuario.id_usuario} asignado al proyecto {proyecto.id_proyecto} como Administrador.\n")

    print("=== 4. Probando Tableros y Listas ===")
    tablero = repo_tablero.crear_tablero(
        id_proyecto=proyecto.id_proyecto,
        titulo="Tablero Principal"
    )
    print(f"✓ Tablero creado -> ID: {tablero.id_tablero}, Título: {tablero.titulo}")

    lista = repo_lista.crear_lista(
        id_tablero=tablero.id_tablero,
        nombre_lista="Por Hacer",
        posicion=1
    )
    print(f"✓ Lista creada -> ID: {lista.id_lista}, Nombre: {lista.nombre_lista}\n")

    print("=== PRUEBA COMPLETADA CON ÉXITO ===")


if __name__ == '__main__':
    probar_sistema()