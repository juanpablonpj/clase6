from blog.datos import cargar_posts_json, guardar_posts_json
from blog.menu import ejecutar_menu
from blog.modelos import Blog


def main() -> None:
    posts = cargar_posts_json()
    blog = Blog(nombre="Blog de Interiorismo y Estilo", posts=posts)
    guardar_posts_json(blog)
    ejecutar_menu(blog)


if __name__ == "__main__":
    main()