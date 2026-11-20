from typing import Any


class ErrorSerializacion(Exception):
    """Error lanzado cuando un objeto no puede serializarse o reconstruirse."""


class Autor:
    """Representa a la persona autora de las publicaciones del blog."""

    def __init__(
        self,
        nombre: str,
        bio: str,
        especialidad: str = "Decoración de interiores de manera profesional",
        redes_sociales: dict[str, str] | None = None,
    ) -> None:
        self.nombre = nombre.strip()
        self.bio = bio.strip()
        self.especialidad = especialidad.strip()
        self.redes_sociales = dict(redes_sociales) if redes_sociales else {}

    def a_diccionario(self) -> dict[str, Any]:
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad": self.especialidad,
            "redes_sociales": dict(self.redes_sociales),
        }

    @classmethod
    def desde_diccionario(cls, data: dict[str, Any]) -> "Autor":
        if not isinstance(data, dict):
            raise ErrorSerializacion("Los datos del autor deben ser un diccionario.")
        if "nombre" not in data or "bio" not in data:
            raise ErrorSerializacion("El diccionario del autor está incompleto (faltan 'nombre' o 'bio').")
        return cls(
            nombre=str(data["nombre"]),
            bio=str(data["bio"]),
            especialidad=str(data.get("especialidad", "Decoración de interiores de manera profesional")),
            redes_sociales=data.get("redes_sociales") if isinstance(data.get("redes_sociales"), dict) else {},
        )

    def __str__(self) -> str:
        return f"{self.nombre} ({self.especialidad})"


class Post:
    """Representa una publicación del blog asociada a un objeto Autor."""

    ESTADOS_VALIDOS = ("borrador", "publicado", "archivado")

    def __init__(
        self,
        id_post: int,
        titulo: str,
        contenido: str,
        autor: Autor,
        tags: set[str] | list[str] | tuple[str, ...] | None = None,
        estado: str = "publicado",
    ) -> None:
        if not isinstance(autor, Autor):
            raise TypeError("El atributo 'autor' debe ser una instancia de la clase Autor.")
        estado_normalizado = estado.strip().lower()
        if estado_normalizado not in self.ESTADOS_VALIDOS:
            estado_normalizado = "borrador"

        self.id = int(id_post)
        self.titulo = titulo.strip()
        self.contenido = contenido.strip()
        self.autor = autor
        self.tags: set[str] = {t.strip().lower() for t in (tags or set()) if str(t).strip()}
        self.estado = estado_normalizado

    def a_diccionario(self) -> dict[str, Any]:
        if not isinstance(self.autor, Autor):
            raise ErrorSerializacion("No se puede serializar el post: 'autor' no es una instancia válida de Autor.")
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.a_diccionario(),
            "tags": sorted(self.tags),
            "estado": self.estado,
        }

    @classmethod
    def desde_diccionario(cls, data: dict[str, Any]) -> "Post":
        if not isinstance(data, dict):
            raise ErrorSerializacion("Cada post en el JSON debe ser un diccionario.")
        requeridos = ("id", "titulo", "contenido", "autor")
        faltantes = [campo for campo in requeridos if campo not in data]
        if faltantes:
            raise ErrorSerializacion(f"Diccionario de post incompleto. Faltan campos: {', '.join(faltantes)}.")

        autor_obj = Autor.desde_diccionario(data["autor"])
        return cls(
            id_post=data["id"],
            titulo=str(data["titulo"]),
            contenido=str(data["contenido"]),
            autor=autor_obj,
            tags=data.get("tags", []),
            estado=str(data.get("estado", "publicado")),
        )


class Blog:
    """Centraliza la colección de objetos Post y las operaciones del blog."""

    def __init__(self, nombre: str, posts: list[Post] | None = None) -> None:
        self.nombre = nombre
        self.posts: list[Post] = []
        if posts:
            for item in posts:
                if not isinstance(item, Post):
                    raise TypeError("Todos los elementos iniciales de 'posts' deben ser instancias de Post.")
                self.posts.append(item)

    def obtener_todos(self) -> list[Post]:
        return list(self.posts)

    def siguiente_id(self) -> int:
        if not self.posts:
            return 1
        return max(post.id for post in self.posts) + 1

    def agregar_post(self, post: Post) -> None:
        if not isinstance(post, Post):
            raise TypeError("Solo se pueden agregar instancias de Post al Blog.")
        self.posts.append(post)

    def crear_post(
        self,
        titulo: str,
        contenido: str,
        autor: Autor,
        tags: set[str] | list[str] | None = None,
        estado: str = "publicado",
    ) -> Post:
        nuevo_post = Post(
            id_post=self.siguiente_id(),
            titulo=titulo,
            contenido=contenido,
            autor=autor,
            tags=tags,
            estado=estado,
        )
        self.agregar_post(nuevo_post)
        return nuevo_post

    def buscar_por_titulo(self, termino: str) -> list[Post]:
        consulta = termino.strip().lower()
        if not consulta:
            return []
        return [post for post in self.posts if consulta in post.titulo.lower()]

    def filtrar_por_tag(self, tag: str) -> list[Post]:
        etiqueta = tag.strip().lower()
        if not etiqueta:
            return []
        return [post for post in self.posts if etiqueta in {t.lower() for t in post.tags}]

    def validar_posts(self) -> list[str]:
        """Devuelve una lista de problemas encontrados; vacía si todos los posts son válidos."""
        problemas: list[str] = []
        if not self.posts:
            problemas.append("No hay posts cargados en el blog.")
            return problemas

        for post in self.posts:
            if not isinstance(post, Post):
                problemas.append("Se encontró un elemento que no es una instancia válida de Post.")
                continue
            if not post.titulo.strip():
                problemas.append(f"Post ID {post.id}: el título está vacío.")
            if not post.contenido.strip():
                problemas.append(f"Post ID {post.id} ('{post.titulo}'): el contenido está vacío.")
            if not isinstance(post.autor, Autor) or not post.autor.nombre.strip():
                problemas.append(f"Post ID {post.id} ('{post.titulo}'): falta un autor válido.")
            if post.estado not in Post.ESTADOS_VALIDOS:
                problemas.append(f"Post ID {post.id} ('{post.titulo}'): estado '{post.estado}' no válido.")
        return problemas

    def a_lista_diccionarios(self) -> list[dict[str, Any]]:
        """Convierte todos los objetos Post a diccionarios listos para JSON."""
        resultado: list[dict[str, Any]] = []
        for post in self.posts:
            if not isinstance(post, Post):
                raise ErrorSerializacion(
                    "Se intentó guardar un objeto que no es una instancia de Post sin convertirlo a diccionario."
                )
            resultado.append(post.a_diccionario())
        return resultado

    @classmethod
    def desde_lista_diccionarios(cls, nombre_blog: str, datos: list[Any]) -> "Blog":
        """Reconstruye un Blog y sus objetos Post/Autor a partir de una lista de diccionarios."""
        if not isinstance(datos, list):
            raise ErrorSerializacion("El contenido JSON de posts debe ser una lista.")
        posts_reconstruidos: list[Post] = []
        for item in datos:
            posts_reconstruidos.append(Post.desde_diccionario(item))
        return cls(nombre=nombre_blog, posts=posts_reconstruidos)
