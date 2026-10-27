class Biblioteca:

    def __init__(self):

        self.libros = []
        self.socios = []

    def agregar_libro(self, libro):

        self.libros[libro.cod_libro] = libro

    def agregar_socio(self, socio):

        self.socios[socio.cod_socio] = socio

    def prestar_libro(self, cod_libro, cod_socio):

        if cod_libro not in self.libros:
            raise ValueError(f"No existe un libro con el código {cod_libro}.")
        if cod_socio not in self.socios:
            raise ValueError(f"No existe un socio con el código {cod_socio}.")
        libro = self.libros[cod_libro]
        socio = self.socios[cod_socio]

        if socio.tiene_libro_prestado():
            raise ValueError(f"El socio '{socio.nombre}' ya tiene un libro prestado (código {socio.cod_libro}).")
        libro.prestar(cod_socio)
        socio.cod_libro = cod_libro

    def devolver_libro(self, cod_libro):

        if cod_libro not in self.libros:
            raise ValueError(f"No existe un libro con el código {cod_libro}.")
        
        libro = self.libros[cod_libro]

        if not libro.esta_prestado():
            raise ValueError(f"El libro '{libro.titulo}' no está prestado.")
        
        cod_socio = libro.cod_socio

        if cod_socio in self.socios:
            self.socios[cod_socio].cod_libro = None

        libro.devolver()

    def buscar_por_titulo(self, titulo):

        titulo_clean = titulo.lower().strip()
        return [libro for libro in self.libros.values() if libro.titulo.lower().strip() == titulo_clean]

    def obtener_socios_con_libros(self):

        return [
            (socio, self.libros[socio.cod_libro])
            for socio in self.socios.values()
            if socio.tiene_libro_prestado() and socio.cod_libro in self.libros
        ]