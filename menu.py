from blog.modelos import Blog
from blog.operaciones import (
    opcion_buscar_por_titulo,
    opcion_crear_nuevo_post,
    opcion_filtrar_por_tag,
    opcion_guardar_json,
    opcion_validar_posts,
    opcion_ver_todos,
)
from blog.validaciones import validar_opcion_menu

OPCIONES_VALIDAS = ("1", "2", "3", "4", "5", "6", "7")


def imprimir_menu(nombre_blog: str) -> None:
    print(f"\n--- MENU DEL BLOG ({nombre_blog}) ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Crear nuevo post")
    print("5. Validar posts")
    print("6. Guardar posts en JSON")
    print("7. Salir")


def ejecutar_menu(blog: Blog) -> None:
    while True:
        imprimir_menu(blog.nombre)
        entrada = input("Elegí una opción: ")
        try:
            opcion = validar_opcion_menu(entrada, OPCIONES_VALIDAS)
        except ValueError as exc:
            print(f"[Error] {exc}")
            continue

        if opcion == "1":
            opcion_ver_todos(blog)
        elif opcion == "2":
            opcion_buscar_por_titulo(blog)
        elif opcion == "3":
            opcion_filtrar_por_tag(blog)
        elif opcion == "4":
            opcion_crear_nuevo_post(blog)
        elif opcion == "5":
            opcion_validar_posts(blog)
        elif opcion == "6":
            opcion_guardar_json(blog)
        elif opcion == "7":
            opcion_guardar_json(blog)
            print("¡Hasta la próxima! Cerrando el sistema de blog.")
            break