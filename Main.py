#Programa hecho por Juan Coll y Valeria Solorzano
import sys
import time as t

print("Iniciando el programa principal...")
print("Intentando cargar datos desde 'Source.cargar_datos'...")

try:
    #Esta línea ejecuta 'cargar_datos.py'
    from Source.cargar_datos import ingredientes, hotdog_seleccionado, inventario
except ImportError as e:
    print(f"{'='*50}")
    print(f"¡ERROR FATAL!: No se pudo encontrar el módulo 'Source.cargar_datos'.")
    print(f"Detalle: {e}")
    print("Asegúrate de estar ejecutando 'main.py' desde el directorio raíz")
    print("y que tu estructura de carpetas sea correcta (ej: /Source/cargar_datos.py).")
    print(f"{'='*50}")
    sys.exit(1)
except Exception as e:
    #Captura cualquier otro error inesperado durante la importación inicial
    print(f"¡ERROR INESPERADO al cargar datos!: {e}")
    sys.exit(1)

#Si llegamos aquí, los datos se cargaron correctamente.
print("Datos cargados. Importando sistema de gestión...")



#Importamos la función que inicia el sub-menú
try:
    from Modules.gestion_de_ingredientes import iniciar_programa_GestorIngredientes
    from Modules.Gestor_de_inventario import iniciar_programa_GestorInventario
    from Modules.Gestor_de_menu import iniciar_programa_GestorMenu
    from Modules.Simular_dia_de_ventas import iniciar_programa_Simulador
except ImportError as e:
    print(f"\n{'='*50}")
    print(f"¡ERROR FATAL!: No se pudo encontrar el módulo 'Modules.gestion_de_ingredientes'.")
    print(f"¡ERROR FATAL!: No se pudo encontrar el módulo 'Modules.Gestor_de_inventario'.")
    print(f"¡ERROR FATAL!: No se pudo encontrar el módulo 'Modules.Gestor_de_menu'.")
    print(f"Detalle: {e}")
    print(f"{'='*50}")
    t.sleep(2)
    sys.exit(1)

print("Sistema de gestión importado con éxito.")


#funcion del menu principal
def main():
    """
    Función principal que actúa como el menú de más alto nivel.
    """
    print("="*50)
    print(" BIENVENIDO AL SISTEMA DE GESTIÓN DE Hot Dog CCS 🌭")
    print("="*50)
    t.sleep(1)
    #Bucle principal de la aplicación
    while True:
        print("--- MENÚ PRINCIPAL ---")
        print("1. Gestionar Ingredientes")
        print("2. Gestionar Inventario")
        print("3. Gestionar Menu")
        print("4. Realizar simulacion de ventas")
        print("5. Salir del programa")
        t.sleep(0.4)
        opcion_principal = input("Seleccione una opción: ")
        
        if opcion_principal == '1':
            iniciar_programa_GestorIngredientes(ingredientes, hotdog_seleccionado)
        elif opcion_principal == '2':
            iniciar_programa_GestorInventario(ingredientes, hotdog_seleccionado)
        elif opcion_principal == '3':
            iniciar_programa_GestorMenu( hotdog_seleccionado,ingredientes)
        elif opcion_principal == '4':
            iniciar_programa_Simulador(ingredientes, hotdog_seleccionado, inventario)    
        elif opcion_principal == '5':
            print("Gracias por usar el sistema. ¡Adiós! ")
            t.sleep(3)
            break
        else:
            print(" Opción no válida. Intente de nuevo.")

if __name__ == "__main__":

    main()

