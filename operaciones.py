from blog.datos import guardar_posts_json
from blog.modelos import Autor, Blog, Post
from blog.validaciones import parsear_tags, validar_texto_no_vacio


def mostrar_posts(posts: list[Post], encabezado: str = "POSTS DEL BLOG") -> None:
    print(f"\n=== {encabezado} ===")
    if not posts:
        print("No se encontraron publicaciones para mostrar.")
        return

    for post in posts:
        tags_str = ", ".join(sorted(post.tags)) if post.tags else "sin etiquetas"
        print(f"- [{post.id}] {post.titulo} | Autor: {post.autor.nombre} | Estado: {post.estado} | Tags: {tags_str}")
        print(f"    {post.contenido}")


def opcion_ver_todos(blog: Blog) -> None:
    mostrar_posts(blog.obtener_todos(), "TODOS LOS POSTS")


def opcion_buscar_por_titulo(blog: Blog) -> None:
    termino = input("Ingresá el título o palabra clave a buscar: ").strip()
    if not termino:
        print("[Aviso] Ingresá un texto para buscar.")
        return
    resultados = blog.buscar_por_titulo(termino)
    mostrar_posts(resultados, f"RESULTADOS PARA '{termino}'")


def opcion_filtrar_por_tag(blog: Blog) -> None:
    etiqueta = input("Ingresá el tag a filtrar: ").strip()
    if not etiqueta:
        print("[Aviso] Ingresá una etiqueta para filtrar.")
        return
    resultados = blog.filtrar_por_tag(etiqueta)
    mostrar_posts(resultados, f"POSTS CON TAG '{etiqueta.lower()}'")


def opcion_crear_nuevo_post(blog: Blog) -> None:
    print("\n--- CREAR NUEVO POST ---")
    try:
        titulo = validar_texto_no_vacio(input("Título: "), "título")
        contenido = validar_texto_no_vacio(input("Contenido: "), "contenido")
        nombre_autor = validar_texto_no_vacio(
            input("Nombre del autor [Enter para 'Aline Npj']: ") or "Aline Npj",
            "nombre del autor",
        )
        bio_autor = input("Bio del autor [Enter para bio por defecto]: ").strip()
        if not bio_autor:
            bio_autor = "Especialista en decoración de interiores de manera profesional."

        tags_raw = input("Etiquetas separadas por coma (ej. living, luz): ")
        estado = input("Estado (publicado / borrador / archivado) [publicado]: ").strip() or "publicado"

        autor_obj = Autor(nombre=nombre_autor, bio=bio_autor)
        nuevo_post = blog.crear_post(
            titulo=titulo,
            contenido=contenido,
            autor=autor_obj,
            tags=parsear_tags(tags_raw),
            estado=estado,
        )
        print(f"[OK] Post creado con ID {nuevo_post.id}: '{nuevo_post.titulo}'.")

        if guardar_posts_json(blog):
            print("[OK] Cambios guardados automáticamente en posts.json.")
    except ValueError as exc:
        print(f"[Error de validación] {exc}")


def opcion_validar_posts(blog: Blog) -> None:
    print("\n--- VALIDACIÓN DE POSTS ---")
    problemas = blog.validar_posts()
    if not problemas:
        print("[OK] Todos los posts del blog son válidos.")
    else:
        for problema in problemas:
            print(f"[!] {problema}")


def opcion_guardar_json(blog: Blog) -> None:
    if guardar_posts_json(blog):
        print("[OK] Posts guardados correctamente en posts.json.")