from blog.modelos import Post


def validar_texto_no_vacio(valor: str, nombre_campo: str) -> str:
    limpio = valor.strip()
    if not limpio:
        raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
    return limpio


def parsear_tags(texto_tags: str) -> set[str]:
    return {tag.strip().lower() for tag in texto_tags.split(",") if tag.strip()}


def validar_opcion_menu(opcion: str, opciones_validas: tuple[str, ...]) -> str:
    limpia = opcion.strip()
    if limpia not in opciones_validas:
        raise ValueError(f"Opción '{limpia}' inválida. Elegí entre: {', '.join(opciones_validas)}.")
    return limpia


def es_post_valido(post: Post) -> tuple[bool, str]:
    if not post.titulo.strip():
        return False, "El título está vacío."
    if not post.contenido.strip():
        return False, "El contenido está vacío."
    if not post.autor.nombre.strip():
        return False, "El nombre del autor está vacío."
    return True, "OK"