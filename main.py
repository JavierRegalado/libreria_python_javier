import os

from modelo.libro import Libro
from modelo.socio import Socio
from modelo.biblioteca import Biblioteca

RUTA_LIBROS = "datos/libros.txt"
RUTA_SOCIOS = "datos/socios.txt"

def cargar_datos():

    if os.path.exists(RUTA_LIBROS):
        contador_libros = 0
        with open(RUTA_LIBROS, mode="r", encoding="UTF-8") as archivo:
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
                Biblioteca.agregar_libro(libro)
                contador_libros += 1

        print(f"Se cargaron {contador_libros} libros")
    else:
        print(f"No se encontró el archivo {RUTA_LIBROS}. No se cargaron libros.")

    if os.path.exists(RUTA_SOCIOS):
        contador_socios = 0
        with open(RUTA_SOCIOS, mode="r", encoding="UTF-8") as archivo:
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
                Biblioteca.agregar_socio(socio)
                contador_socios += 1

        print(f"Se cargaron {contador_socios} socios")
    else:
        print(f"No se encontró el archivo {RUTA_SOCIOS}. No se cargaron socios.")

    def guardar_datos():
        os.makedirs(os.path.dirname(RUTA_LIBROS), exist_ok=True)

        with open(RUTA_LIBROS, mode="w", encoding="UTF-8") as f:
            for libro in Biblioteca.libros.values():
                cod_socio_str = str(libro.cod_socio) if libro.cod_socio is not None else ""
                f.write(f"{libro.cod_libro};{libro.titulo};{libro.autor};{libro.año};{libro.categoria};{cod_socio_str}\n")

        with open(RUTA_SOCIOS, mode="w", encoding="UTF-8") as f:
            for socio in Biblioteca.socios.values():
                cod_libro_str = str(socio.cod_libro) if socio.cod_libro is not None else ""
                f.write(f"{socio.cod_socio};{socio.nombre};{socio.email};{cod_libro_str}\n")

        print("Datos guardados correctamente en los archivos.")

    def mostrar_tabla_libros():
        print(f"\n--- Tabla de Libros ---")

        if not Biblioteca.libros:
            print("No hay libros registrados.")
            return

        print(f"{'Código':<10} | {'Título':<30} | {'Autor':<20} | {'Año':<6} | {'Categoría':<15} | {'Prestado a':<15}")
        print("-" * 110)
        for libro in Biblioteca.libros.values():
            cod_socio_str = str(libro.cod_socio) if libro.cod_socio is not None else "Disponible"
            print(f"{libro.cod_libro:<10} | {libro.titulo:<30} | {libro.autor:<20} | {libro.año:<6} | {libro.categoria:<15} | {cod_socio_str:<15}")

    def mostrar_tabla_socios():
        print(f"\n--- Tabla de Socios ---")

        if not Biblioteca.socios:
            print("No hay socios registrados.")
            return

        print(f"{'Código':<10} | {'Nombre':<30} | {'Email':<30} | {'Libro Prestado':<15}")
        print("-" * 100)
        for socio in Biblioteca.socios.values():
            cod_libro_str = str(socio.cod_libro) if socio.cod_libro is not None else "Ninguno"
            print(f"{socio.cod_socio:<10} | {socio.nombre:<30} | {socio.email:<30} | {cod_libro_str:<15}")

    def main():
        cargar_datos()
        mostrar_tabla_libros()
        mostrar_tabla_socios()
        guardar_datos()

    if __name__ == "__main__":
        main()