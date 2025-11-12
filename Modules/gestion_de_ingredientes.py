import time as t

from Source.cargar_datos import ingredientes, hotdog_seleccionado, inventario

from Source.Gestion_archivos import guardar_todo



class GestorIngredientes:
    def __init__(self, ingredientes,menu):
        self.ingredientes = ingredientes
        self.menu=menu


    def listar(self):   
        """Muestra todos los ingredientes organizados por categoría.""" 
        print("\n📦 LISTA COMPLETA DE INGREDIENTES")
        print("=" * 50)

        # Configuración para cada categoría
        config_categorias = {
            "Pan": {"emoji": "🥖", "tipo": "normal"},
            "Salchicha": {"emoji": "🌭", "tipo": "normal"},
            "Acompañante": {"emoji": "🍟", "tipo": "normal"},
            "Salsa": {"emoji": "🥫", "tipo": "salsa"},
            "toppings": {"emoji": "🧅", "tipo": "topping"}
        }

        for categoria_data in self.ingredientes:
            nombre_categoria = categoria_data["Categoria"]

            if nombre_categoria in config_categorias:
                config = config_categorias[nombre_categoria]
                emoji = config["emoji"]
                tipo_formato = config["tipo"]

                print(f"\n{emoji} CATEGORÍA {nombre_categoria.upper()}")
                print("-" * (15 + len(nombre_categoria)))

                for opcion in categoria_data["Opciones"]:
                    if tipo_formato == "normal":
                        print(f"* {opcion['nombre']} ({opcion['tipo']}, {opcion['tamaño']} {opcion['unidad']})")
                    elif tipo_formato == "salsa":
                        print(f"* {opcion['nombre']} (Base: {opcion['base']}, Color: {opcion['color']})")
                    elif tipo_formato == "topping":
                        print(f"* {opcion['nombre']} ({opcion['tipo']}, {opcion['presentación']})")
        
    def listar_por_categoria(self):
       
        """Muestra los ingredientes organizados y agrupados por tipo dentro de cada categoría.

        Para cada categoría (Pan, Salchicha, Topping, Salsa, Acompañante):
        - Agrupa los ingredientes por su tipo/base
        - Muestra cuántos productos hay de cada tipo
        - Permite navegar entre categorías interactivamente
        """

    # Configuración de categorías
        
        categorias = {
        "1": {"indice": 0, "nombre": "Pan 🥖", "clasificador": "tipo", "tipo": "normal"},
        "2": {"indice": 1, "nombre": "Salchicha 🌭", "clasificador": "tipo", "tipo": "normal"},
        "3": {"indice": 2, "nombre": "Topping 🍟,🥤", "clasificador": "tipo", "tipo": "normal"},
        "4": {"indice": 3, "nombre": "Salsa 🥫", "clasificador": "base", "tipo": "salsa"},
        "5": {"indice": 4, "nombre": "Acompañante 🧅", "clasificador": "tipo", "tipo": "acompanante"}
    }
    
        while True:
            print("""\n📋 Indique qué ingredientes desea ver:
        1) Pan 🥖
        2) Salchicha 🌭
        3) Topping 🍟,🥤
        4) Salsa 🥫
        5) Acompañante 🧅
        6) Salir ❌""")
            
            opcion = input("→ ")
            
            if opcion == "6":
                print("👋 ¡Hasta luego!")
                break
            
            if opcion in categorias:
                cat_config = categorias[opcion]
                idx = cat_config["indice"]
                tipos_vistos = []
                
                print(f"\n{'='*50}")
                print(f"📂 CATEGORÍA: {cat_config['nombre']}")
                print(f"{'='*50}")
                
                #Buscar el tipo que se va a listar

                for ingrediente in self.ingredientes[idx]["Opciones"]:
                    tipo_actual = ingrediente[cat_config["clasificador"]]
                    
                    if tipo_actual not in tipos_vistos:
                        # Contar ingredientes de este tipo
                        cont =0
                        for k in self.ingredientes[idx]["Opciones"] :
                                     if k[cat_config["clasificador"]] == tipo_actual:
                                         cont+=1
                   
                        # Encabezado del tipo
            
                        print(f"\n📁 Tipo: {tipo_actual}")
                        print(f"{'-'*30}")
                        
                        # Listar todos los ingredientes de este tipo
                        for k in self.ingredientes[idx]["Opciones"]:
                            if k[cat_config["clasificador"]] == tipo_actual:
                                # Formatear según el tipo de categoría
                                if cat_config["tipo"] == "salsa":
                                    print(f"* {k['nombre']} (Base:{k['base']}, Color:{k['color']})")
                                elif cat_config["tipo"] == "acompanante":
                                    print(f"* {k['nombre']} ({k['tipo']}, {k['presentación']})")
                                else:
                                    print(f"* {k['nombre']} ({k['tipo']}, {k['tamaño']} {k['unidad']})")
                        
                        # Mostrar contador
                        print(f"\n📊 Total: {cont} producto(s) de este tipo")
                        tipos_vistos.append(tipo_actual)
                
                if not tipos_vistos:
                    print("ℹ️  No hay ingredientes en esta categoría")
                    
            else:
                print("❌ Opción incorrecta, asegúrese de colocar una de las opciones que aparece en la pantalla\n")
    
    def agregar(self):
            
        """Permite agregar un nuevo ingrediente al sistema organizado por categorías."""

        print("""\n📦 AGREGAR NUEVO INGREDIENTE
Indique la categoría:
1) Pan 🥖
2) Salchicha 🌭
3) Topping 🍟
4) Salsa 🥫
5) Acompañante 🧅
6) Cancelar ❌""")
    
        opcion = input("→ ")

        if opcion == "6":
            print("❌ Operación cancelada")
            return

        categorias_map = {
            "1": {"indice": 0, "nombre": "Pan", "emoji": "🥖"},
            "2": {"indice": 1, "nombre": "Salchicha", "emoji": "🌭"},
            "3": {"indice": 2, "nombre": "Topping", "emoji": "🍟"},
            "4": {"indice": 3, "nombre": "Salsa", "emoji": "🥫"},
            "5": {"indice": 4, "nombre": "Acompañante", "emoji": "🧅"}
        }

        if opcion in categorias_map:
            cat_config = categorias_map[opcion]
            idx = cat_config["indice"]
            nombre_categoria = cat_config["nombre"]
            emoji = cat_config["emoji"]

            print(f"\n{emoji} AGREGAR NUEVO {nombre_categoria.upper()}")
            print("=" * 40)

            # Datos comunes
            nombre = input("Nombre del nuevo ingrediente: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío")
                return

            # Verificar si el nombre ya existe
            i = 0
            while i < len(self.ingredientes[idx]["Opciones"]):
                if self.ingredientes[idx]["Opciones"][i]["nombre"].lower() == nombre.lower():
                    print(f"❌ Ya existe un {nombre_categoria.lower()} con ese nombre")
                    return
                i += 1

            nuevo_ingrediente = {"nombre": nombre}

            # Campos específicos por categoría
            if opcion in ["1", "2", "3"]:  # Pan, Salchicha, Topping
                tipo = input("Tipo del ingrediente: ").strip()
                tamaño = input("Tamaño del ingrediente: ").strip()
                unidad = input("Unidad del ingrediente: ").strip()

                nuevo_ingrediente["tipo"] = tipo.capitalize() if opcion == "3" else tipo.lower()
                nuevo_ingrediente["tamaño"] = tamaño
                nuevo_ingrediente["unidad"] = unidad

            elif opcion == "4":  # Salsa
                base = input("Base de la salsa: ").strip()
                color = input("Color de la salsa: ").strip()

                nuevo_ingrediente["base"] = base.capitalize()
                nuevo_ingrediente["color"] = color

            elif opcion == "5":  # Acompañante
                tipo = input("Tipo del acompañante: ").strip()
                preparacion = input("Preparación del acompañante: ").strip()

                nuevo_ingrediente["tipo"] = tipo.capitalize()
                nuevo_ingrediente["preparación"] = preparacion

            # Agregar a la lista
            self.ingredientes[idx]["Opciones"].append(nuevo_ingrediente)

            # Inicializar en inventario
            inventario[nombre] = 0

            print(f"✅ {nombre_categoria} '{nombre}' registrado correctamente")
            print(f"📝 Se ha inicializado en inventario con 0 unidades")

        else:
            print("❌ Opción incorrecta, seleccione una de las opciones mostradas")
    
    #Funcion extre para eliminar
    def buscar_hotdogs_con_ingrediente(self, categoria, nombre_ingrediente):
        """Busca y retorna todos los hot dogs que utilizan un ingrediente específico"""
   
        hotdogs_afectados = []
    
        i = 0
        while i < len(self.menu):
            hotdog = self.menu[i]

            if categoria == "Pan" and hotdog["Pan"] == nombre_ingrediente:
                hotdogs_afectados.append(hotdog)
            elif categoria == "Salchicha" and hotdog["Salchicha"] == nombre_ingrediente:
                hotdogs_afectados.append(hotdog)
            elif categoria == "Topping" and nombre_ingrediente in hotdog.get("toppings", []):
                hotdogs_afectados.append(hotdog)
            elif categoria == "Salsa" and nombre_ingrediente in hotdog.get("salsas", []):
                hotdogs_afectados.append(hotdog)
            elif categoria == "Acompañante" and hotdog.get("Acompañante") == nombre_ingrediente:
                hotdogs_afectados.append(hotdog)

            i += 1

        return hotdogs_afectados


    def eliminar(self):
    
        """Elimina un ingrediente del sistema con validación de uso en hot dogs"""

        opciones_map = {
                "1": 0,  # Pan
                "2": 1,  # Salchicha
                "3": 2,  # Topping
                "4": 3,  # Salsa
                "5": 4   # Acompañante
            }

        print("""\n📋 Indique qué ingredientes desea eliminar:
        1) Pan 🥖
        2) Salchicha 🌭
        3) Topping 🍟,🥤
        4) Salsa 🥫
        5) Acompañante 🧅
        6) Salir ❌""")
    
        opcion = input("→ ")
        
        if opcion == "6":
            return
        
        if opcion in opciones_map:
            categoria_idx = opciones_map[opcion]
            categoria_nombre = ["Pan", "Salchicha", "Topping", "Salsa", "Acompañante"][categoria_idx]
            
            print(f"\nOpciones de {categoria_nombre}:")
            cont = 0
            i = 0
            while i < len(self.ingredientes[categoria_idx]["Opciones"]):
                cont += 1
                print(f"{cont}) {self.ingredientes[categoria_idx]['Opciones'][i]['nombre']}")
                i += 1
                
            try:
                seleccion = int(input(f"\nPresione el número del {categoria_nombre} que desea eliminar: "))
                
                if 1 <= seleccion <= len(self.ingredientes[categoria_idx]["Opciones"]):
                    ingrediente_a_eliminar = self.ingredientes[categoria_idx]["Opciones"][seleccion - 1]
                    nombre_ingrediente = ingrediente_a_eliminar['nombre']
                    
                    # VERIFICAR SI EL INGREDIENTE ESTÁ EN USO
                    hotdogs_afectados = self.buscar_hotdogs_con_ingrediente(categoria_nombre, nombre_ingrediente)
                    
                    if hotdogs_afectados:
                        # Mostrar hot dogs que serán eliminados
                        print(f"\n⚠️  ADVERTENCIA: El ingrediente '{nombre_ingrediente}' está en uso")
                        print(f"   Hot dogs que serán eliminados:")
                        j = 0
                        while j < len(hotdogs_afectados):
                            print(f"   • {hotdogs_afectados[j]['nombre']}")
                            j += 1
                        
                        print(f"\n¿Está seguro que desea eliminar '{nombre_ingrediente}'?")
                        print("   Esto eliminará el ingrediente y los hot dogs relacionados")
                        print("1. Sí, eliminar ingrediente y hot dogs")
                        print("2. No, cancelar eliminación")
                        
                        confirmacion = input("→ ")
                        
                        if confirmacion == "1":
                            # Eliminar el ingrediente
                            ingrediente_eliminado = self.ingredientes[categoria_idx]["Opciones"].pop(seleccion - 1)
                            
                            # Eliminar los hot dogs afectados
                            k = 0
                            while k < len(hotdogs_afectados):
                                self.menu.remove(hotdogs_afectados[k])
                                k += 1
                                
                            print(f"✓ {nombre_ingrediente} eliminado correctamente")
                            print(f"✓ {len(hotdogs_afectados)} hot dog(s) eliminado(s) del menú")
                            
                        else:
                            print("❌ Eliminación cancelada")
                            
                    else:
                        # El ingrediente no está en uso, eliminar directamente
                        ingrediente_eliminado = self.ingredientes[categoria_idx]["Opciones"].pop(seleccion - 1)
                        print(f"✓ {ingrediente_eliminado['nombre']} eliminado correctamente")
                        
                else:
                    print("❌ Número fuera de rango")
                    
            except ValueError:
                print("❌ Error: Debe ingresar un número válido")
        else:
            print("❌ Opción no válida")



def iniciar_programa_GestorIngredientes(ingredientes_data, menu_data):
    # 1. Creamos la instancia y le pasamos los datos
    gestor = GestorIngredientes(ingredientes_data, menu_data)
        
        # 2. Bucle del menú de gestión
    while True:
        print("\n--- MENÚ DE GESTIÓN DE INGREDIENTES ---")
        print("1. Listar todos los ingredientes")
        print("2. Listar ingredientes por categoría (agrupado)")
        print("3. Agregar nuevo ingrediente")
        print("4. Eliminar ingrediente")
        print("5. Volver al menú principal")
            
        opcion = input("Seleccione una opción: ")
            
        if opcion == '1':
            gestor.listar()
            t.sleep(1)
        elif opcion == '2':
            gestor.listar_por_categoria()
            t.sleep(1)
        elif opcion == '3':
            gestor.agregar()
            t.sleep(1)
        elif opcion == '4':
            gestor.eliminar()
            t.sleep(1)
        elif opcion == '5':
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







                


