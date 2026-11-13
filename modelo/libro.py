class Libro:
    def __init__(self, cod_libro, titulo, autor, año, categoria, cod_socio=None):
        self.cod_libro = cod_libro
        self.titulo = titulo
        self.autor = autor
        self.año = año
        self.categoria = categoria
        self.cod_socio = cod_socio

    def __str__(self):
        return f"Libro(cod_libro={self.cod_libro}, titulo='{self.titulo}', autor='{self.autor}', año={self.año}, categoria='{self.categoria}', cod_socio={self.cod_socio})"

    def esta_prestado(self):
        return self.cod_socio is not None

    def prestar(self, cod_socio):
        if self.esta_prestado():
            raise ValueError(f"El libro '{self.titulo}' ya está prestado al socio con código {self.cod_socio}.")
        self.cod_socio = cod_socio

    def devolver(self):
        if not self.esta_prestado():
            raise ValueError(f"El libro '{self.titulo}' no está prestado.")
        self.cod_socio = None