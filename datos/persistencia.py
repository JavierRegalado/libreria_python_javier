from datetime import datetime
import os
from modelo.libro import Libro
from modelo.socio import Socio

RUTA_LIBROS = "datos/libros.txt"
RUTA_SOCIOS = "datos/socios.txt"


def cargar_datos(biblioteca):
    contador_libros = 0
    contador_socios = 0

    if os.path.exists(RUTA_LIBROS):
        with open(RUTA_LIBROS, mode="r", encoding="UTF-8-SIG") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(";")
                cod_libro = int(partes[0])
                titulo = partes[1]
                autor = partes[2]
                año = int(partes[3])
                categoria = partes[4]
                cod_socio = int(partes[5]) if len(partes) > 5 and partes[5] else None

                libro = Libro(cod_libro, titulo, autor, año, categoria, cod_socio)
                biblioteca.libros[libro.cod_libro] = libro
                contador_libros += 1

    if os.path.exists(RUTA_SOCIOS):
        with open(RUTA_SOCIOS, mode="r", encoding="UTF-8-SIG") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(";")
                cod_socio = int(partes[0])
                nombre = partes[1]
                email = partes[2]
                cod_libro = int(partes[3]) if len(partes) > 3 and partes[3] else None

                socio = Socio(cod_socio, nombre, email, cod_libro)
                biblioteca.socios[socio.cod_socio] = socio
                contador_socios += 1

    return contador_libros, contador_socios


def guardar_datos(biblioteca):
    os.makedirs(os.path.dirname(RUTA_LIBROS), exist_ok=True)

    with open(RUTA_LIBROS, mode="w", encoding="UTF-8-SIG") as f:
        for libro in biblioteca.libros.values():
            cod_socio_str = str(libro.cod_socio) if libro.cod_socio is not None else ""
            f.write(f"{libro.cod_libro};{libro.titulo};{libro.autor};{libro.año};{libro.categoria};{cod_socio_str}\n")

    with open(RUTA_SOCIOS, mode="w", encoding="UTF-8-SIG") as f:
        for socio in biblioteca.socios.values():
            cod_libro_str = str(socio.cod_libro) if socio.cod_libro is not None else ""
            f.write(f"{socio.cod_socio};{socio.nombre};{socio.email};{cod_libro_str}\n")

def registrar_evento(evento, detalles):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("log.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}][{evento}][{detalles}]\n")