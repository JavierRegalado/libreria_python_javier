class Socio:
    def __init__(self, cod_socio, nombre, email, cod_libro=None):
        self.cod_socio = cod_socio
        self.nombre = nombre
        self.email = email
        self.cod_libro = cod_libro

    def __str__(self):
        return f"Socio(cod_socio={self.cod_socio}, nombre='{self.nombre}', email='{self.email}', cod_libro={self.cod_libro})"

    def tiene_libro_prestado(self):
        return self.cod_libro is not None