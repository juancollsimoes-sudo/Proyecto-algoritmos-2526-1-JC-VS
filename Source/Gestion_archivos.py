#Programa hecho por Juan Coll y Valeria Solorzano
#Módulo para guardar los datos (ingredientes, menu, inventario) en sus respectivos archivos JSON locales.


import os
import json
script_path = os.path.abspath(__file__)
source_dir = os.path.dirname(script_path)
#Subir un nivel para llegar al directorio raíz del proyecto
proyecto_raiz = os.path.dirname(source_dir)
#Apuntar a la carpeta 'Data'
Data_Dir = os.path.join(proyecto_raiz, "Data")

#Definir las rutas completas de guardado
guardar_ingredientes = os.path.join(Data_Dir, "ingredientes.json")
guardar_menu = os.path.join(Data_Dir, "menu.json")
guardar_inventario = os.path.join(Data_Dir, "inventario.json")



def guardar_todo(ingredientes_modificados, menu_modificado, inventario_modificado):

    #Guarda las listas de ingredientes, menú e inventario en sus archivos JSON.

    print("Iniciando el guardado de datos...")
    exito_i, exito_m, exito_inv = False, False, False

    try:
        #Guardar Ingredientes
        with open(guardar_ingredientes, 'w', encoding='utf-8') as f:
            json.dump(ingredientes_modificados, f, indent=4, ensure_ascii=False)
        exito_i = True #Si llegamos aquí, fue exitoso
        #Guardar Menú
        with open(guardar_menu, 'w', encoding='utf-8') as f:
            json.dump(menu_modificado, f, indent=4, ensure_ascii=False)
        exito_m = True #Si llegamos aquí, fue exitoso
        #Guardar Inventario
        with open(guardar_inventario, 'w', encoding='utf-8') as f:
            json.dump(inventario_modificado, f, indent=4, ensure_ascii=False)
        exito_inv = True #Si llegamos aquí, fue exitoso

        if exito_i and exito_m and exito_inv:
            print("Se han guardado 'ingredientes.json', 'menu.json' e 'inventario.json' exitosamente.")
            return True
        else:
            if not exito_i:
                print("FALLO al guardar 'ingredientes.json'.")
            if not exito_m:
                print("FALLO al guardar 'menu.json'.")
            if not exito_inv:
                print("FALLO al guardar 'inventario.json'.")
            return False
            
    except (IOError, TypeError) as e: #Capturamos errores de escritura o tipo
        print(f"¡ERROR CRÍTICO AL GUARDAR!: {e}")

        return False

