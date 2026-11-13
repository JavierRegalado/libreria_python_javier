class BibliotecaError(Exception):
    pass

class LibroNoEncontradoError(BibliotecaError):
    def __init__(self, cod_libro):
        super().__init__(f"No se encontro ningun libro con ese codigo")
        self.cod_libro = cod_libro

class SocioNoEncontradoError(BibliotecaError):
    def __init__(self, cod_socio):
        super().__init__(f"No se encontró ningún socio con el código.")
        self.cod_socio = cod_socio


class LibroYaPrestadoError(BibliotecaError):
    def __init__(self, titulo, cod_socio):
        super().__init__(f"El libro '{titulo}' ya está prestado al socio con código {cod_socio}.")


class SocioConLibroError(BibliotecaError):
    def __init__(self, nombre_socio, cod_libro):
        super().__init__(f"El socio '{nombre_socio}' ya tiene prestado el libro con código {cod_libro}.")


class SocioSinLibroError(BibliotecaError):
    def __init__(self, nombre_socio):
        super().__init__(f"El socio '{nombre_socio}' no tiene ningún libro prestado para devolver.")


class CodigoExistenteError(BibliotecaError):
    def __init__(self, tipo_entidad, codigo):
        super().__init__(f"Ya existe un(a) {tipo_entidad} registrado(a) con el código {codigo}.")