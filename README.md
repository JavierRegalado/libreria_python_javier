# Sistema de Gestión de Biblioteca

Aplicación de consola (CLI) en Python con arquitectura modular para gestionar el catálogo de libros, socios y préstamos de una biblioteca, con persistencia en archivos de texto y registro de auditoría.


## Funcionamiento de la Aplicación

* **Ciclo de datos**: Al iniciar (`main.py` → `iniciar_aplicacion()`), carga `datos/libros.txt` y `datos/socios.txt` (delimitados por `;` en `UTF-8-SIG`) en memoria. Los cambios se guardan en disco al seleccionar la opción **8. Salir**.
* **Auditoría**: Cada alta, préstamo o devolución registra una línea en `log.txt` con formato `[YYYY-MM-DD HH:MM:SS][EVENTO][DETALLES]`.
* **Funcionalidades del menú**:
  1. Listar todos los libros y su estado (`Disponible` o código del socio).
  2. Listar solo libros disponibles.
  3. Buscar libros por título.
  4. Registrar préstamos (vincular libro y socio).
  5. Registrar devoluciones a partir del código de socio.
  6. Listar socios con préstamos activos.
  7. Dar de alta nuevos libros y socios.
* **Reglas de negocio**: Mediante excepciones personalizadas (`BibliotecaError`), se bloquean códigos duplicados, operaciones sobre registros inexistentes, préstamos de ejemplares ocupados y más de **1 libro simultáneo por socio**.

## Ejecución

Requiere **Python 3.8+** (sin dependencias externas). Desde la raíz del proyecto:

```bash
python main.py
```

## Posibles Mejoras para el Repositorio

### Correcciones Prioritarias
* **Búsqueda por título (`modelo/biblioteca.py`)**: Invertir la condición en `buscar_libros_por_titulo` a `titulo_clean in libro.titulo.lower().strip()` para permitir búsquedas parciales.
* **Persistencia inmediata (`view/vista.py`)**: Llamar a `persistencia.guardar_datos()` tras cada alta, préstamo o devolución para evitar pérdida de datos ante cierres inesperados.
* **Encapsulación (`modelo/biblioteca.py`)**: Usar `libro.prestar(cod_socio)` dentro de `prestar_libro` en lugar de modificar `libro.cod_socio` directamente.
* **Mensajes de error (`errores/excepciones.py` / `view/vista.py`)**: Mostrar el código buscado en `LibroNoEncontradoError` y `SocioNoEncontradoError`, y separar el `ValueError` del `año` respecto al del código de libro al dar de alta.

### Arquitectura y Nuevas Funcionalidades
* **Almacenamiento robusto**: Migrar de `.txt` manual a `csv`, `json` o `sqlite3` para evitar fallos si algún campo contiene `;`.
* **Validaciones y logging**: Validar cadenas vacías y formato de email, reemplazar el log manual por el módulo estándar `logging` y añadir un `.gitignore` (`__pycache__/`, `log.txt`).
* **Ampliación funcional**: Permitir múltiples préstamos por socio, añadir fechas de vencimiento, implementar edición/borrado (CRUD) e incorporar tests unitarios (`pytest` o `unittest`).

### Video Explicativo
[Click aqui para ver el video explicativo de la apliacacion] (https://drive.google.com/file/d/1dz1GmMZ_T15cQoNo1QKJD6wG70b99QaW/view?usp=sharing)
