import json
from pathlib import Path
from typing import Any

from blog.modelos import Autor, Blog, ErrorSerializacion, Post

RUTA_POSTS_JSON = Path(__file__).resolve().parent.parent / "posts.json"


def posts_iniciales_por_defecto() -> list[Post]:
    autor_aline = Autor(
        nombre="Aline Npj",
        bio="Especialista en diseño y ambientación de espacios residenciales y comerciales.",
        especialidad="Decoración de interiores de manera profesional",
        redes_sociales={"instagram": "@alinenpj.deco"},
    )
    return [
        Post(
            id_post=1,
            titulo="Iluminación cálida en livings modernos",
            contenido="Combinar luz indirecta con lámparas de pie aporta calidez sin perder amplitud visual.",
            autor=autor_aline,
            tags={"iluminacion", "living", "interiorismo"},
            estado="publicado",
        ),
        Post(
            id_post=2,
            titulo="Texturas naturales y paletas neutras",
            contenido="El lino, la madera clara y los tonos arena ayudan a construir ambientes serenos y atemporales.",
            autor=autor_aline,
            tags={"texturas", "neutros", "decoracion"},
            estado="publicado",
        ),
    ]


def cargar_posts_json(ruta: Path = RUTA_POSTS_JSON) -> list[Post]:
    """Carga posts desde posts.json y los reconstruye como objetos Post."""
    if not ruta.exists():
        print(f"[Aviso] No se encontró '{ruta.name}'. Se iniciará con posts base.")
        return posts_iniciales_por_defecto()

    try:
        contenido = ruta.read_text(encoding="utf-8").strip()
        if not contenido:
            print(f"[Aviso] El archivo '{ruta.name}' está vacío. Se iniciará con posts base.")
            return posts_iniciales_por_defecto()

        datos_raw: Any = json.loads(contenido)
        if not isinstance(datos_raw, list):
            print(f"[Aviso] '{ruta.name}' no contiene una lista válida. Se iniciará con posts base.")
            return posts_iniciales_por_defecto()

        posts_cargados: list[Post] = []
        for indice, item in enumerate(datos_raw, start=1):
            try:
                posts_cargados.append(Post.desde_diccionario(item))
            except ErrorSerializacion as exc:
                print(f"[Aviso] Registro #{indice} omitido por datos incompletos o inválidos: {exc}")
        return posts_cargados

    except json.JSONDecodeError as exc:
        print(f"[Aviso] El archivo '{ruta.name}' tiene JSON inválido ({exc}). Se iniciará con posts base.")
        return posts_iniciales_por_defecto()
    except OSError as exc:
        print(f"[Error] No se pudo leer '{ruta.name}': {exc}")
        return posts_iniciales_por_defecto()


def guardar_posts_json(blog: Blog, ruta: Path = RUTA_POSTS_JSON) -> bool:
    """Convierte los objetos Post del Blog a diccionarios y los guarda en posts.json."""
    try:
        datos_serializables = blog.a_lista_diccionarios()
        ruta.write_text(
            json.dumps(datos_serializables, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True
    except ErrorSerializacion as exc:
        print(f"[Error de serialización] {exc}")
        return False
    except OSError as exc:
        print(f"[Error de archivo] No se pudo escribir en '{ruta.name}': {exc}")
        return False