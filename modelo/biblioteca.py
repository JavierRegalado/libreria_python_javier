from modelo.libro import Libro
from modelo.socio import Socio
from errores.excepciones import (
    LibroNoEncontradoError,
    SocioNoEncontradoError,
    LibroYaPrestadoError,
    SocioConLibroError,
    SocioSinLibroError,
    CodigoExistenteError,
)


class Biblioteca:

    def __init__(self):

        self.libros = {}
        self.socios = {}

    def registrar_libro(self, libro):

        if libro.cod_libro in self.libros:
            raise CodigoExistenteError("libro", libro.cod_libro)
        
        self.libros[libro.cod_libro] = libro
        return libro

    def registrar_socio(self, socio):

        if socio.cod_socio in self.socios:
            raise CodigoExistenteError("socio", socio.cod_socio)

        self.socios[socio.cod_socio] = socio
        return socio

    def obtener_libros_disponibles(self):
        return [libro for libro in self.libros.values() if not libro.esta_prestado()]

    def buscar_libros_por_titulo(self, titulo):
        titulo_clean = titulo.lower().strip()
        return [libro for libro in self.libros.values() if libro.titulo.lower().strip() in titulo_clean]

    def prestar_libro(self, cod_libro, cod_socio):

        libro = self.libros.get(cod_libro)
        socio = self.socios.get(cod_socio)

        if not libro:
            raise LibroNoEncontradoError(cod_libro)
        if not socio:
            raise SocioNoEncontradoError(cod_socio)
        if libro.esta_prestado():
            raise LibroYaPrestadoError(libro.titulo, libro.cod_socio)
        if socio.tiene_libro_prestado():
            raise SocioConLibroError(socio.nombre, socio.cod_libro)

        libro.cod_socio = cod_socio
        socio.cod_libro = cod_libro

        return libro, socio

        
    def devolver_libro(self, cod_socio):

        socio = self.socios.get(cod_socio)

        if not socio:
            raise SocioNoEncontradoError(cod_socio)
        if not socio.cod_libro:
            raise SocioSinLibroError(socio.nombre)

        cod_libro = socio.cod_libro
        libro = self.libros.get(cod_libro)

        if libro:
            libro.devolver()
        socio.cod_libro = None

        return libro, socio, cod_libro


    def obtener_socios_con_libros(self):

        return [socio for socio in self.socios.values() if socio.tiene_libro_prestado()]