import os
from modelo.biblioteca import Biblioteca
import datos.persistencia as persistencia
from errores.excepciones import BibliotecaError
from modelo.libro import Libro
from modelo.socio import Socio

def mostrar_menu_principal():
    print("\n" + "=" * 50)
    print("              GESTIÓN DE BIBLIOTECA - MENÚ")
    print("=" * 50)
    print("1. Mostrar todos los libros")
    print("2. Mostrar libros disponibles")
    print("3. Buscar libro por título")
    print("4. Prestar un libro")
    print("5. Devolver un libro")
    print("6. Mostrar todos los socios con libros prestados")
    print("7. Añadir libros y socios")
    print("8. Salir")
    print("=" * 50)
    return input("Seleccione una opción (1-8): ")

def mostrar_libros(biblioteca):
    print("\n--- LISTA DE LIBROS ---")
    if not biblioteca.libros:
        print("No hay libros registrados en la biblioteca.")
        return
    print(f"{'Código':<10}{'Título':<30}{'Autor':<20}{'Año':<6}{'Categoría':<15}{'Código Socio':<15}")
    print("-" * 100)
    for libro in biblioteca.libros.values():
        socio_str = str(libro.cod_socio) if libro.cod_socio is not None else "Disponible"
        print(f"{libro.cod_libro:<10}{libro.titulo:<30}{libro.autor:<20}{libro.año:<6}{libro.categoria:<15}{socio_str:<15}")

def mostrar_libros_disponibles(biblioteca):
    print("\n--- LIBROS DISPONIBLES ---")
    libros_disponibles = biblioteca.obtener_libros_disponibles()
    if not libros_disponibles:
        print("No hay libros disponibles en este momento.")
        return
    print(f"{'Código':<10}{'Título':<30}{'Autor':<20}{'Año':<6}{'Categoría':<15}")
    print("-" * 90)
    for libro in libros_disponibles:
        print(f"{libro.cod_libro:<10}{libro.titulo:<30}{libro.autor:<20}{libro.año:<6}{libro.categoria:<15}")

def buscar_libro_por_titulo(biblioteca):
    print("\n--- BUSCAR LIBRO POR TÍTULO ---")
    titulo = input("Ingrese el título del libro a buscar: ")
    libros_encontrados = biblioteca.buscar_libros_por_titulo(titulo)
    if not libros_encontrados:
        print(f"No se encontraron libros con el título '{titulo}'.")
        return
    print(f"{'Código':<10}{'Título':<30}{'Autor':<20}{'Año':<6}{'Categoría':<15}{'Estado':<15}")
    print("-" * 100)
    for libro in libros_encontrados:
        estado = "Prestado" if libro.esta_prestado() else "Disponible"
        print(f"{libro.cod_libro:<10}{libro.titulo:<30}{libro.autor:<20}{libro.año:<6}{libro.categoria:<15}{estado:<15}")

def prestar_libro(biblioteca):
    print("\n--- PRESTAR UN LIBRO ---")
    try:
        cod_libro = int(input("Ingrese el código del libro: "))
        cod_socio = int(input("Ingrese el código del socio: "))
        libro, socio = biblioteca.prestar_libro(cod_libro, cod_socio)
        print(f"El libro '{libro.titulo}' ha sido prestado al socio '{socio.nombre}'.")
    except ValueError:
        print("Error: Los códigos deben ser números enteros.")
    except BibliotecaError as e:
        print(f"Error: {e}")

def devolver_libro(biblioteca):
    print("\n--- DEVOLVER UN LIBRO ---")
    try:
        cod_socio = int(input("Ingrese el código del socio: "))
        libro, socio, cod_libro = biblioteca.devolver_libro(cod_socio)
        print(f"El libro '{libro.titulo}' ha sido devuelto por el socio '{socio.nombre}'.")
    except ValueError:
        print("Error: El código del socio debe ser un número entero.")
    except BibliotecaError as e:
        print(f"Error: {e}")

def mostrar_socios_con_libros(biblioteca):
    print("\n--- SOCIOS CON LIBROS PRESTADOS ---")
    socios_con_libros = biblioteca.obtener_socios_con_libros()
    if not socios_con_libros:
        print("No hay socios con libros prestados.")
        return
    print(f"{'Código Socio':<15}{'Nombre':<30}{'Email':<30}{'Código Libro':<15}{'Título Libro':<30}")
    print("-" * 120)
    for socio in socios_con_libros:
        libro = biblioteca.libros.get(socio.cod_libro)
        titulo_libro = libro.titulo if libro else "Desconocido"
        print(f"{socio.cod_socio:<15}{socio.nombre:<30}{socio.email:<30}{socio.cod_libro:<15}{titulo_libro:<30}")

def menu_añadir_libros_y_socios(biblioteca):
    while True:
        print("\n--- AÑADIR LIBROS Y SOCIOS ---")
        print("1. Añadir un libro")
        print("2. Añadir un socio")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == "1":
            try:
                cod_libro = int(input("Ingrese el código del libro: "))
                titulo = input("Ingrese el título del libro: ")
                autor = input("Ingrese el autor del libro: ")
                año = int(input("Ingrese el año de publicación: "))
                categoria = input("Ingrese la categoría del libro: ")
                libro = biblioteca.registrar_libro(Libro(cod_libro, titulo, autor, año, categoria))
                print(f"Libro '{libro.titulo}' registrado exitosamente.")
            except ValueError:
                print("Error: Los códigos deben ser números enteros.")
            except BibliotecaError as e:
                print(f"Error: {e}")
        elif opcion == "2":
            try:
                cod_socio = int(input("Ingrese el código del socio: "))
                nombre = input("Ingrese el nombre del socio: ")
                email = input("Ingrese el email del socio: ")
                socio = biblioteca.registrar_socio(Socio(cod_socio, nombre, email))
                print(f"Socio '{socio.nombre}' registrado exitosamente.")
            except ValueError:
                print("Error: El código del socio debe ser un número entero.")
            except BibliotecaError as e:
                print(f"Error: {e}")
        elif opcion == "3":
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def iniciar_aplicacion():
    biblioteca = Biblioteca()
    persistencia.cargar_datos(biblioteca)

    while True:
        opcion = mostrar_menu_principal()

        if opcion == "1":
            mostrar_libros(biblioteca)
        elif opcion == "2":
            mostrar_libros_disponibles(biblioteca)
        elif opcion == "3":
            buscar_libro_por_titulo(biblioteca)
        elif opcion == "4":
            prestar_libro(biblioteca)
        elif opcion == "5":
            devolver_libro(biblioteca)
        elif opcion == "6":
            mostrar_socios_con_libros(biblioteca)
        elif opcion == "7":
            menu_añadir_libros_y_socios(biblioteca)
        elif opcion == "8":
            persistencia.guardar_datos(biblioteca)
            print("Saliendo de la aplicación. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")