import os

from modelo.libro import Libro
from modelo.socio import Socio
from modelo.biblioteca import Biblioteca

RUTA_LIBROS = "datos/libros.txt"
RUTA_SOCIOS = "datos/socios.txt"

biblioteca = Biblioteca()


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
                biblioteca.agregar_libro(libro)
                contador_libros += 1
        print(f"Se cargaron {contador_libros} libros.")
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
                biblioteca.agregar_socio(socio)
                contador_socios += 1
        print(f"Se cargaron {contador_socios} socios.")
    else:
        print(f"No se encontró el archivo {RUTA_SOCIOS}. No se cargaron socios.")


def guardar_datos():
    os.makedirs(os.path.dirname(RUTA_LIBROS), exist_ok=True)

    with open(RUTA_LIBROS, mode="w", encoding="UTF-8") as f:
        for libro in biblioteca.libros.values():
            cod_socio_str = str(libro.cod_socio) if libro.cod_socio is not None else ""
            f.write(f"{libro.cod_libro};{libro.titulo};{libro.autor};{libro.año};{libro.categoria};{cod_socio_str}\n")

    with open(RUTA_SOCIOS, mode="w", encoding="UTF-8") as f:
        for socio in biblioteca.socios.values():
            cod_libro_str = str(socio.cod_libro) if socio.cod_libro is not None else ""
            f.write(f"{socio.cod_socio};{socio.nombre};{socio.email};{cod_libro_str}\n")

    print("\nDatos guardados correctamente en los archivos.")


def mostrar_todos_los_libros():
    print("\n--- LISTA DE TODOS LOS LIBROS ---")
    if not biblioteca.libros:
        print("No hay libros registrados.")
        return

    print(f"{'Código':<8} | {'Título':<30} | {'Autor':<20} | {'Categoría':<15} | {'Estado':<15}")
    print("-" * 95)
    for libro in biblioteca.libros.values():
        estado = f"Prestado a {libro.cod_socio}" if libro.cod_socio is not None else "Disponible"
        print(f"{libro.cod_libro:<8} | {libro.titulo[:28]:<30} | {libro.autor[:18]:<20} | {libro.categoria[:13]:<15} | {estado:<15}")

def mostrar_libros_disponibles():
    print("\n--- LIBROS DISPONIBLES ---")
    disponibles = [l for l in biblioteca.libros.values() if l.cod_socio is None]

    if not disponibles:
        print("No hay libros disponibles actualmente.")
        return

    print(f"{'Código':<8} | {'Título':<30} | {'Autor':<20} | {'Categoría':<15}")
    print("-" * 80)
    for libro in disponibles:
        print(f"{libro.cod_libro:<8} | {libro.titulo[:28]:<30} | {libro.autor[:18]:<20} | {libro.categoria[:13]:<15}")


def buscar_libro_por_titulo():
    print("\n--- BUSCAR LIBRO ---")
    busqueda = input("Ingrese el término de búsqueda para el título: ").strip().lower()

    if not busqueda:
        print("Debe ingresar un término válido.")
        return

    resultados = [l for l in biblioteca.libros.values() if busqueda in l.titulo.lower()]

    if not resultados:
        print(f"No se encontró ningún libro que contenga '{busqueda}' en el título.")
        return

    print(f"\nResultados encontrados ({len(resultados)}):")
    print(f"{'Código':<8} | {'Título':<30} | {'Autor':<20} | {'Año':<6} | {'Estado':<15}")
    print("-" * 85)
    for libro in resultados:
        estado = f"Prestado (Socio: {libro.cod_socio})" if libro.cod_socio is not None else "Disponible"
        print(f"{libro.cod_libro:<8} | {libro.titulo[:28]:<30} | {libro.autor[:18]:<20} | {libro.año:<6} | {estado:<15}")



def prestar_libro():
    print("\n--- PRESTAR UN LIBRO ---")
    try:
        cod_libro = int(input("Ingrese el código del libro: "))
        cod_socio = int(input("Ingrese el código del socio: "))
    except ValueError:
        print("Error: Los códigos deben ser números enteros.")
        return

    libro = biblioteca.libros.get(cod_libro)
    socio = biblioteca.socios.get(cod_socio)

    if not libro:
        print(f"Error: El libro con código {cod_libro} no existe.")
        return

    if not socio:
        print(f"Error: El socio con código {cod_socio} no existe.")
        return

    if libro.cod_socio is not None:
        print(f"Error: El libro '{libro.titulo}' ya está prestado al socio con código {libro.cod_socio}.")
        return

    if socio.cod_libro is not None:
        print(f"Error: El socio '{socio.nombre}' ya tiene prestado el libro con código {socio.cod_libro}.")
        return


    libro.cod_socio = socio.cod_socio
    socio.cod_libro = libro.cod_libro
    print(f"El libro '{libro.titulo}' ha sido prestado a '{socio.nombre}'.")



def devolver_libro():
    print("\n--- DEVOLVER UN LIBRO ---")
    try:
        cod_socio = int(input("Ingrese el código del socio: "))
    except ValueError:
        print("Error: El código debe ser un número entero.")
        return

    socio = biblioteca.socios.get(cod_socio)

    if not socio:
        print(f"Error: El socio con código {cod_socio} no existe.")
        return

    if socio.cod_libro is None:
        print(f"El socio '{socio.nombre}' no tiene ningún libro prestado actualmente.")
        return

    cod_libro = socio.cod_libro
    libro = biblioteca.libros.get(cod_libro)


    if libro:
        libro.cod_socio = None
    socio.cod_libro = None

    titulo_libro = libro.titulo if libro else f"Código {cod_libro}"
    print(f"Se ha devuelto el libro '{titulo_libro}' prestado a '{socio.nombre}'.")


def mostrar_socios_con_prestamos():
    print("\n--- SOCIOS CON LIBROS PRESTADOS ---")
    socios_con_libro = [s for s in biblioteca.socios.values() if s.cod_libro is not None]

    if not socios_con_libro:
        print("No hay ningún socio con libros prestados actualmente.")
        return

    print(f"{'Código Socio':<12} | {'Nombre Socio':<25} | {'Cód. Libro':<10} | {'Título del Libro':<30}")
    print("-" * 85)
    for socio in socios_con_libro:
        libro = biblioteca.libros.get(socio.cod_libro)
        titulo_libro = libro.titulo if libro else "Título no encontrado"
        print(f"{socio.cod_socio:<12} | {socio.nombre[:23]:<25} | {socio.cod_libro:<10} | {titulo_libro[:28]:<30}")



def menu_añadir_registros():
    while True:
        print("\n--- AÑADIR REGISTROS ---")
        print("1. Añadir un nuevo Libro")
        print("2. Añadir un nuevo Socio")
        print("3. Volver al menú principal")

        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            try:
                cod_libro = int(input("Código del libro: "))
                if cod_libro in biblioteca.libros:
                    print(f"[!] Error: Ya existe un libro con el código {cod_libro}.")
                    continue

                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                año = int(input("Año de publicación: "))
                categoria = input("Categoría: ").strip()

                nuevo_libro = Libro(cod_libro, titulo, autor, año, categoria)
                biblioteca.agregar_libro(nuevo_libro)
                print(f"Libro '{titulo}' registrado con éxito.")
            except ValueError:
                print("Error: Los campos 'código' y 'año' deben ser números.")

        elif opcion == "2":
            try:
                cod_socio = int(input("Código del socio: "))
                if cod_socio in biblioteca.socios:
                    print(f"Error: Ya existe un socio con el código {cod_socio}.")
                    continue

                nombre = input("Nombre completo: ").strip()
                email = input("Email: ").strip()

                nuevo_socio = Socio(cod_socio, nombre, email)
                biblioteca.agregar_socio(nuevo_socio)
                print(f"Socio '{nombre}' registrado con éxito.")
            except ValueError:
                print("Error: El código debe ser un número entero.")

        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def mostrar_menu_principal():
    print("\n" + "=" * 45)
    print("       GESTIÓN DE BIBLIOTECA - MENÚ")
    print("=" * 45)
    print("1. Mostrar todos los libros")
    print("2. Mostrar libros disponibles")
    print("3. Buscar libro por título")
    print("4. Prestar un libro a un socio")
    print("5. Devolver un libro")
    print("6. Mostrar socios con libros prestados")
    print("7. Añadir socios y libros")
    print("8. Guardar y salir")
    print("=" * 45)


def main():
    cargar_datos()

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-8): ").strip()

        if opcion == "1":
            mostrar_todos_los_libros()
        elif opcion == "2":
            mostrar_libros_disponibles()
        elif opcion == "3":
            buscar_libro_por_titulo()
        elif opcion == "4":
            prestar_libro()
        elif opcion == "5":
            devolver_libro()
        elif opcion == "6":
            mostrar_socios_con_prestamos()
        elif opcion == "7":
            menu_añadir_registros()
        elif opcion == "8":
            guardar_datos()
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, introduzca un número del 1 al 8.")


if __name__ == "__main__":
    main()