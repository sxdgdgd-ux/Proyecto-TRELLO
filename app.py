"""Script de pruebas de integracion para consultar los datos en MySQL usando Peewee."""
from Datos.modelos.models import (
    Usuario,
    Proyecto,
    Tablero,
    Lista,
    Tarjeta,
    Etiqueta,
    Comentario,
    ProyectoUsuario,
    AsignacionTarjeta,
    TarjetaEtiqueta,
)


def consultar_y_verificar_datos():
    """Realiza consultas en todas las tablas para validar el funcionamiento del ORM."""
    print("==================================================")
    print(" 🚀 INICIANDO PRUEBAS DE LECTURA EN MYSQL")
    print("==================================================\n")

    # 1. Consultar Usuarios
    print("--- 1. USUARIOS REGISTRADOS ---")
    usuarios = Usuario.select()
    for u in usuarios:
        print(f"  • ID: {u.id_usuario} | Nombre: {u.nombre} | Email: {u.email}")
    print(f"Total: {len(usuarios)} usuarios.\n")

    # 2. Consultar Proyectos y sus Miembros
    print("--- 2. PROYECTOS Y SUS MIEMBROS ---")
    proyectos = Proyecto.select()
    for p in proyectos:
        print(f"\n📌 Proyecto ID {p.id_proyecto}: {p.nombre_proyecto}")
        print(f"   Descripción: {p.descripcion}")
        
        miembros = (
            ProyectoUsuario.select(ProyectoUsuario, Usuario)
            .join(Usuario)
            .where(ProyectoUsuario.id_proyecto == p.id_proyecto)
        )
        print("   Miembros asignados:")
        for m in miembros:
            print(f"     - {m.id_usuario.nombre} (Rol: {m.rol})")

    # 3. Consultar Tableros, Listas y Tarjetas
    print("\n--- 3. ESTRUCTURA DE TABLEROS, LISTAS Y TARJETAS ---")
    tableros = Tablero.select()
    for t in tableros:
        print(f"\n📋 Tablero ID {t.id_tablero}: '{t.titulo}' (Proyecto: {t.id_proyecto.nombre_proyecto})")
        
        listas = Lista.select().where(Lista.id_tablero == t.id_tablero).order_by(Lista.posicion)
        for l in listas:
            print(f"   📂 Lista ID {l.id_lista}: [{l.nombre_lista}] (Posición: {l.posicion})")
            
            tarjetas = Tarjeta.select().where(Tarjeta.id_lista == l.id_lista)
            for tar in tarjetas:
                print(f"      🎴 Tarjeta ID {tar.id_tarjeta}: '{tar.titulo}' | Estado: {tar.estado}")
                
                asignaciones = (
                    AsignacionTarjeta.select(AsignacionTarjeta, Usuario)
                    .join(Usuario)
                    .where(AsignacionTarjeta.id_tarjeta == tar.id_tarjeta)
                )
                usuarios_asignados = [a.id_usuario.nombre for a in asignaciones]
                if usuarios_asignados:
                    print(f"         👤 Asignado a: {', '.join(usuarios_asignados)}")

                etiquetas_rel = (
                    TarjetaEtiqueta.select(TarjetaEtiqueta, Etiqueta)
                    .join(Etiqueta)
                    .where(TarjetaEtiqueta.id_tarjeta == tar.id_tarjeta)
                )
                etiquetas_nombres = [te.id_etiqueta.nombre for te in etiquetas_rel]
                if etiquetas_nombres:
                    print(f"         🏷️  Etiquetas: {', '.join(etiquetas_nombres)}")

                comentarios = Comentario.select().where(Comentario.id_tarjeta == tar.id_tarjeta)
                for c in comentarios:
                    print(f"         💬 Comentario ({c.id_usuario.nombre}): \"{c.texto}\"")

    print("\n==================================================")
    print(" 🎉 ¡CONSULTA REALIZADA CON ÉXITO! EL CÓDIGO Y LAS TABLAS FUNCIONAN CORRECTAMENTE.")
    print("==================================================")


if __name__ == '__main__':
    consultar_y_verificar_datos()