

from .Lector_GitHub import LectorDelRepositorio
import sys

print("Módulo 'datos.py' cargando archivos locales...")


lector = LectorDelRepositorio(dueño="", nombre_repo="") # No importa el dueño/repo aquí

# Definimos los nombres de los archivos
ingredientes_local = "Data/ingredientes.json"
menu_local = "Data/menu.json"
inventario_local = "Data/inventario.json"

# Cargamos los datos en variables 
ingredientes = lector.cargar_archivo_local(ingredientes_local)
hotdog_seleccionado= lector.cargar_archivo_local(menu_local)
inventario = lector.cargar_archivo_local(inventario_local)

if inventario is None:
    # Si no existe, o está vacío/corrupto, creamos uno nuevo.
    print("No se encontró 'inventario.json', se creará uno nuevo.")
    inventario = {}


# Verificación de seguridad
if ingredientes is None or hotdog_seleccionado is None:
    print("-------------------------------------------------")
    print("¡ERROR FATAL en cargar_datos.py!")
    print("No se pudieron cargar 'ingredientes.json' o 'menu.json'.")
    print("¡Asegúrate de ejecutar 'descargar_datos.py' primero!")
    print("-------------------------------------------------")
    sys.exit(1) # Detiene todo si los datos no existen
else:
    print("Datos (INGREDIENTES, MENU Y INVENTARIO) cargados con éxito.")


    