#Programa hecho por Juan Coll y Valeria Solorzano
#Programa descargador

#Importamos la "herramienta" del archivo anterior
from Lector_GitHub import LectorDelRepositorio

#Configuración
dueño = "FernandoSapient" 
nombre_repo = "BPTSP05_2526-1"
branch = "main"
ingredientes_remoto = "ingredientes.json"
menu_remoto = "menu.json"
ingredientes_local = "Data/ingredientes.json"
menu_local = "Data/menu.json"

#Creamos la instancia
lector = LectorDelRepositorio(dueño=dueño, nombre_repo=nombre_repo, branch=branch)

print("--- Ejecutando el DESCARGADOR ---")
print("Descargando archivos de GitHub...")

#Llamamos a la función de descarga
exito1 = lector.descargar_y_guardar_archivo(ingredientes_remoto, ingredientes_local)
exito2 = lector.descargar_y_guardar_archivo(menu_remoto, menu_local)

if exito1 and exito2:
    print("¡Descarga completada! Los archivos .json están listos.")
else:

    print("¡Fallo la descarga! Revisa los errores.")

