#Programa hecho por Juan Coll y Valeria Solorzano
import time as t


from Source.cargar_datos import ingredientes, hotdog_seleccionado, inventario

from Source.Gestion_archivos import guardar_todo





class GestorInventario:
    def __init__(self, ingredientes,inventario):
        self.ingredientes = ingredientes
        self.inventario=inventario
        
    
    def inicializar_inventario(self):
        """Inicializa el inventario con cantidades aleatorias para todos los ingredientes existentes"""
        for categoria in ingredientes:
            for opcion in categoria["Opciones"]:
                # Asignar cantidades iniciales basadas en el tipo de ingrediente
                if categoria["Categoria"] == "Pan":
                    inventario[opcion["nombre"]] = 20
                elif categoria["Categoria"] == "Salchicha":
                    inventario[opcion["nombre"]] = 15
                elif categoria["Categoria"] == "toppings":
                    inventario[opcion["nombre"]] = 30
                elif categoria["Categoria"] == "Salsa":
                    inventario[opcion["nombre"]] = 10
                elif categoria["Categoria"] == "Acompañante":
                    inventario[opcion["nombre"]] = 25
        return inventario
    
    def visualizar_inventario(self):

        """Muestra una vista completa y organizada de todo el inventario disponible"""

        total_general = 0
        categorias_contadas = 0
        
        for categoria in ingredientes:
            nombre_categoria = categoria["Categoria"]
            total_categoria = 0
           

            print(f"\n 🗂️  {nombre_categoria.upper()}")
            print("-" * 40)

            for opcion in categoria["Opciones"]:
                    nombre = opcion["nombre"]
                    cantidad = inventario.get(nombre, 0)
                    total_categoria += cantidad
                    
                    if  nombre_categoria == "Pan":
                            print(f"   🥖 {nombre}: {cantidad} unidades")
                    elif nombre_categoria == "Salchicha":
                            print(f"   🌭 {nombre}: {cantidad} unidades")
                    elif nombre_categoria == "Salsa":
                            print(f"   🥫 {nombre}: {cantidad} unidades")
                    elif nombre_categoria == "toppings":
                                print(f"   🧅 {nombre}: {cantidad} unidades")
                    elif nombre_categoria == "Acompañante":
                                print(f"   🍟 {nombre}: {cantidad} unidades")
            
            print(f"   📊 Total {nombre_categoria}: {total_categoria} unidades")

            total_general += total_categoria
            categorias_contadas += 1
        
        print(f"\n{'='*60}")
        print(f"📈 TOTAL GENERAL: {total_general} unidades")
        print(f"📋 Productos diferentes: {len(inventario)}")
        print(f"🏷️  Categorías: {categorias_contadas}")


    def ingrediente_especifico(self):

        """Permite buscar y visualizar información detallada de un ingrediente específico en el inventario"""

        print("BUSCAR INGREDIENTE EN INVENTARIO")
        nombre_buscar = input("Ingrese el nombre del ingrediente: ").strip().lower()
        encontrado=False

        for categoria in ingredientes:
            for opcion in categoria["Opciones"]:
                if opcion["nombre"].lower() == nombre_buscar:
                    print(f"\n✅ INGREDIENTE ENCONTRADO:")
                    print(f"   Nombre: {opcion['nombre']}")
                    print(f"   Categoría: {categoria['Categoria']}")
                    print(f"   Cantidad en inventario: {inventario[opcion['nombre']]} unidades")
                    if "tipo" in opcion:
                        print(f"   Tipo: {opcion['tipo']}")
                    if "tamaño" in opcion:
                        print(f"   Tamaño: {opcion['tamaño']} {opcion.get('unidad', '')}")
                    encontrado=True
                    break
        if encontrado ==False:
                     print(f"❌ No se encontró el ingrediente: '{nombre_buscar}'")

    def listar_inventario(self):
        
        """Muestra el inventario completo organizado por categorías con información detallada"""

        opciones_map = {
        "1": 0,  # Pan
        "2": 1,  # Salchicha
        "3": 2,  # Topping
        "4": 3,  # Salsa
        "5": 4   # Acompañante
    }


    
        while True:
            print("""\n📋 Indique qué ingredientes desea ver:
        1) Pan 🥖
        2) Salchicha 🌭
        3) Topping 🍟,🥤
        4) Salsa 🥫
        5) Acompañante 🧅
        6) Salir ❌""")
            
            
            opcion=input("→")
            if opcion == "6":
                print("👋 ¡Hasta luego!")
                break
    
            if opcion in opciones_map:
                categoria_idx = opciones_map[opcion]
                categoria_nombre = ["Pan", "Salchicha", "Topping", "Salsa", "Acompañante"][categoria_idx]
    
    
                for categoria in ingredientes:
                    nombre_categoria= categoria["Categoria"]
                    if nombre_categoria==categoria_nombre:
                        print("-" * 40)
                        print(f"🗂️  {nombre_categoria.upper()}")
                        print("-" * 40)
                        for opcion in categoria["Opciones"]:
                            nombre = opcion["nombre"]



                            print(f"  {nombre.capitalize()}:{inventario.get(nombre, 0)}")

            else:
                print("Opción incorrecta, asegúrese de colocar una de las opciones que aparece en la pantalla\n")
                 
    def actualizar_existencia(self):

        """Permite actualizar manualmente la cantidad en inventario de un ingrediente específico"""
        
        print("ACTUALIZAR EXISTENCIAS")
        
        # Mostrar lista de ingredientes para referencia
        todos_ingredientes = []
        for categoria in self.ingredientes:
            for opcion in categoria["Opciones"]:
                todos_ingredientes.append(opcion["nombre"])
                
        print("Ingredientes disponibles:")

        for i in range(todos_ingredientes.__len__()):
            print(f"{i+1} ) {todos_ingredientes[i]}")

        if len(todos_ingredientes) > 10:
                print(f"   ... y {len(todos_ingredientes)-10} más")

        nombre_ingrediente = input("\nNombre del ingrediente a actualizar: ").strip()
        
        # Verificar que el ingrediente existe
        ingrediente_encontrado = False
        for categoria in ingredientes:
            for opcion in categoria["Opciones"]:
                if opcion["nombre"] == nombre_ingrediente:
                    ingrediente_encontrado = True
                    break
            if ingrediente_encontrado:
                break
    
        if not ingrediente_encontrado:
            print("El ingrediente no existe en la lista de ingredientes")
            return
        try:
            nueva_cantidad = int(input(f"Nueva cantidad para '{nombre_ingrediente}': "))
            if nueva_cantidad < 0:
                print("La cantidad no puede ser negativa")
                return
            
            inventario[nombre_ingrediente] = nueva_cantidad
            print(f"✅ Inventario actualizado: {nombre_ingrediente} = {nueva_cantidad} unidades")
            
        except ValueError:
            print("Ingrese una cantidad válida")

def iniciar_programa_GestorInventario(ingredientes_data, menu_data):
    #Creamos la instancia y le pasamos los datos
    gestor = GestorInventario(ingredientes_data, inventario)       
        #Bucle del menú de gestión
    while True:
        print("\n--- MENÚ DE GESTIÓN DE INVENTARIO ---")
        print("1. inicializar inventario")
        print("2. visualizar inventario")
        print("3. ingrediente especifico")
        print("4. listar inventario")
        print("5. actualizar existencia")
        print("6. salir del programa")
            
            
        opcion = input("Seleccione una opción: ")
            
        if opcion == '1':
            gestor.inicializar_inventario()
            t.sleep(1)
        elif opcion == '2':
            gestor.visualizar_inventario()
            t.sleep(1)
        elif opcion == '3':
            gestor.ingrediente_especifico()
            t.sleep(1)
        elif opcion == '4':
            gestor.listar_inventario()
            t.sleep(1)
        elif opcion == '5':
            gestor.actualizar_existencia()
            t.sleep(1)
        elif opcion == '6':
            try:
                guardar_todo(ingredientes_data, menu_data, inventario)
            except Exception as e:
                print(f"¡ERROR CRÍTICO AL INTENTAR GUARDAR!: {e}")
                print("Los cambios podrían no ser permanentes.")

            print("Regresando al menú principal...")
            t.sleep(2)
            break 
        else:
            print("Opción no válida. Intente de nuevo.")





