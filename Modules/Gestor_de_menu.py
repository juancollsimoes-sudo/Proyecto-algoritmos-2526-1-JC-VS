from Source.cargar_datos import ingredientes, hotdog_seleccionado, inventario

from Source.Gestion_archivos import guardar_todo

import time as t
class GestorMenu:
    

    def __init__(self,menu,ingredientes):
        self.menu=menu
        self.ingredientes=ingredientes

    #Funciones para ver_lista

    def obtener_emoji(self, nombre):

        """Retorna el emoji correspondiente al nombre de un hot dog para mejorar la visualización"""

        banderas = {
            "inglés": "🇬🇧",
            "lederhosen": "🇩🇪", 
            "bonjour": "🇫🇷",
            "varsovia": "🇵🇱",
            "fitness": "💪",
            "soirée": "🎭",
            "coctel": "🥂",
            "coliseo": "🇮🇹",
            "mama mia": "🍝"
        }
        return banderas.get(nombre.lower(), "🌭")    

    def obtener_info_ingrediente(self, categoria, nombre):

        """Obtiene y formatea la información detallada de un ingrediente específico"""

        for cat in ingredientes:
            if cat["Categoria"] == categoria:
                for opcion in cat["Opciones"]:
                    if opcion["nombre"] == nombre:
                        if categoria == "Salsa":
                            return f"{nombre} (Base: {opcion['base']})"
                        elif categoria == "toppings":
                            return f"{nombre} ({opcion['presentación']})"
                        else:
                            tipo = opcion.get('tipo', '')
                            tamaño = opcion.get('tamaño', '')
                            unidad = opcion.get('unidad', '')
                            if tipo and tamaño:
                                return f"{nombre} ({tipo}, {tamaño} {unidad})"
                            elif tipo:
                                return f"{nombre} ({tipo})"
                            else:
                                return nombre
        return nombre
        
    def ver_lista(self,hotdog_seleccionado):

        """Muestra la lista completa de hot dogs disponibles en el menú con formato visual atractivo"""

        # Para hacer esta función, use dos funciones más aparte
        #Una que me dijera que emoji usar (simplemente parte estetica)
        #Otra que va recorriendo la lista de ingredientes, para dar los ingredientes espesificos del hotdog

        print("🌭 MENÚ DE HOT DOGS")
        print("=="*50)
        for i in range(hotdog_seleccionado.__len__()):
            
            print(f"\n{i+1}. {hotdog_seleccionado[i]['nombre'].upper()} {self.obtener_emoji(hotdog_seleccionado[i]['nombre'])}")
            
            # Pan
            pan_info = self.obtener_info_ingrediente("Pan", hotdog_seleccionado[i]["Pan"])
            print(f"   • Pan: {pan_info}")
            
            # Salchicha
            salchicha_info = self.obtener_info_ingrediente("Salchicha", hotdog_seleccionado[i]["Salchicha"])
            print(f"   • Salchicha: {salchicha_info}")
            
            # Toppings
            toppings = hotdog_seleccionado[i].get("toppings", hotdog_seleccionado[i].get("Toppings", []))
            if toppings:
                print(f"   • Toppings: ✅ {', '.join(toppings)}")
            else:
                print(f"   • Toppings: 🚫 Ninguno")
            
            # Salsas
            salsas = hotdog_seleccionado[i].get("salsas", hotdog_seleccionado[i].get("Salsas", []))
            if salsas:
                print(f"   • Salsas: ✅ {', '.join(salsas)}")
            else:
                print(f"   • Salsas: 🚫 Ninguna")
            
            # Acompañante
            acompanante = hotdog_seleccionado[i].get("Acompañante")
            if acompanante:
                acompanante_info = self.obtener_info_ingrediente("Acompañante", acompanante)
                print(f"   • Acompañante: ✅ {acompanante_info}")
            else:
                print(f"   • Acompañante: 🚫 Ninguno")

    #Funcion para mostrar__verificacion_inventario
    def ver_hotdog_espesifico(self,hotdog_seleccionado):

        """Permite visualizar los detalles completos de un hot dog específico del menú"""


        #Para no hacer la función más larga, lo dividi en dos parte
        #Una que simplemente busque el nombre del hotdog
        #Y despues cuando la encuentre, use otra función que garantice si hay ingredientes suficientes 
        
        print("VERIFICAR INVENTARIO PARA VENTA")
        print("=" * 50)
        for i in range(hotdog_seleccionado.__len__()):
            emoji = self.obtener_emoji(hotdog_seleccionado[i]['nombre'])
            print(f"{i+1}. {hotdog_seleccionado[i]['nombre'].upper()} {emoji}")
        print("0. Volver al menú principal")

    
        try:
            opcion = int(input("→ "))
            if opcion == 0:
                return
            if 1 <= opcion <= len(hotdog_seleccionado):
                hotdog_seleccionado = hotdog_seleccionado[opcion-1]
                self.mostrar_verificacion_inventario(hotdog_seleccionado)
            else:
                print("Opción no válida")
        except ValueError:
            print("Ingrese un número válido")

    def mostrar_verificacion_inventario(self,hotdog_seleccionado):

        """Muestra la verificación del estado del inventario"""

        # Verificar cada ingrediente
        problemas = []
        stock_bajo = []

        # Verificar Pan
        pan = hotdog_seleccionado["Pan"]
        stock_pan = inventario.get(pan, 0)
        pan_ok = stock_pan > 0

        # Verificar Salchicha
        salchicha = hotdog_seleccionado["Salchicha"]
        stock_salchicha = inventario.get(salchicha, 0)
        salchicha_ok = stock_salchicha > 0


        # Verificar Toppings
        toppings = hotdog_seleccionado.get("toppings", hotdog_seleccionado.get("Toppings", []))
        toppings_estado = []
        for topping in toppings:
            stock = inventario.get(topping, 0)
            if stock == 0:
                problemas.append(f"FALTANTE: {topping} (0 unidades)")
                toppings_estado.append((topping, False, stock))
            elif stock <= 2:
                stock_bajo.append(f"STOCK CRÍTICO: {topping} (solo {stock} unidad{'es' if stock != 1 else ''})")
                toppings_estado.append((topping, True, stock))
            else:
                toppings_estado.append((topping, True, stock))
    
        # Verificar Salsas
        salsas = hotdog_seleccionado.get("salsas", hotdog_seleccionado.get("Salsas", []))
        salsas_estado = []
        for salsa in salsas:
            stock = inventario.get(salsa, 0)
            if stock == 0:
                problemas.append(f"FALTANTE: {salsa} (0 unidades)")
                salsas_estado.append((salsa, False, stock))
            elif stock <= 3:
                stock_bajo.append(f"STOCK BAJO: {salsa} (solo {stock} unidades)")
                salsas_estado.append((salsa, True, stock))
            else:
                salsas_estado.append((salsa, True, stock))



        # Verificar Acompañante
        acompanante = hotdog_seleccionado.get("Acompañante")
        acompanante_ok = True
        stock_acompanante = 0
        if acompanante:
            stock_acompanante = inventario.get(acompanante, 0)
            acompanante_ok = stock_acompanante > 0
            if not acompanante_ok:
                problemas.append(f"FALTANTE: {acompanante} (0 unidades)")

        # Determinar estado general
        toppings_ok = True
        for estado in toppings_estado:
            if not estado[1]:  # Si algún topping no está OK
                toppings_ok = False
                break
            
        # Verificar si TODAS las salsas están OK  
        salsas_ok = True
        for estado in salsas_estado:
            if not estado[1]:  # Si alguna salsa no está OK
                salsas_ok = False
                break
            
        # Estado general
        todos_ok = (pan_ok and salchicha_ok and toppings_ok and salsas_ok and acompanante_ok)


        # Mostrar resultado
        emoji = self.obtener_emoji(hotdog_seleccionado['nombre'])
        if todos_ok:
            print(f"INVENTARIO SUFICIENTE - {hotdog_seleccionado['nombre'].upper()} {emoji}")
        else:
            print(f"INVENTARIO INSUFICIENTE - {hotdog_seleccionado['nombre'].upper()} {emoji}")

        print("=" * 60)
        print("📋 ESTADO DE INGREDIENTES:")

        # Pan
        
        if pan_ok:
             icono = "✅" 
        else :
            icono = "❌"
            print(f"├─ 🥖 Pan {pan}: {icono} {stock_pan} unidad{'es' if stock_pan != 1 else ''}")

        # Salchicha
        if pan_ok:
             icono = "✅" 
        else :
            icono = "❌"
            print(f"├─ 🌭 Salchicha {salchicha}: {icono} {stock_salchicha} unidad{'es' if stock_salchicha != 1 else ''}")



         # Toppings
        if toppings_estado:
            print("├─ 🍟 Toppings:")
            i = 0
            while i < len(toppings_estado):
                topping = toppings_estado[i][0]
                ok = toppings_estado[i][1]
                stock = toppings_estado[i][2]

                icono = "✅" if ok else "❌"

                # Determinar el prefijo (último elemento o no)
                if i == len(toppings_estado) - 1:
                    prefix = "│  └─"
                else:
                    prefix = "│  ├─"

                # Determinar singular o plural
                if stock == 1:
                    unidades = "unidad"
                else:
                    unidades = "unidades"

                print(f"{prefix} {topping}: {icono} {stock} {unidades}")
                i += 1
        else:
            print("├─ 🍟 Toppings: 🚫 Ninguno")

        # Salsas
        if salsas_estado:
            print("├─ 🥫 Salsas:")

            i = 0
            total_salsas = len(salsas_estado)
            while i < total_salsas:
                salsa = salsas_estado[i][0]
                ok = salsas_estado[i][1]
                stock = salsas_estado[i][2]

                icono = "✅" if ok else "❌"

                # Determinar si es el último elemento
                if i == total_salsas - 1:
                    prefix = "│  └─"
                else:
                    prefix = "│  ├─"

                # Verificar stock bajo
                estado_extra = ""
                if ok and stock <= 3:
                    estado_extra = " (STOCK BAJO)"

                # Determinar singular o plural
                if stock == 1:
                    unidades = "unidad"
                else:
                    unidades = "unidades"

                print(f"{prefix} {salsa}: {icono} {stock} {unidades}{estado_extra}")
                i += 1
        else:
            print("├─ 🥫 Salsas: 🚫 Ninguna")

        # Acompañante
        if acompanante:
            icono = "✅" if acompanante_ok else "❌"

            if stock_acompanante == 1:
                unidades = "unidad"
            else:
                unidades = "unidades"

            print(f"└─ 🧅 Acompañante {acompanante}: {icono} {stock_acompanante} {unidades}")
        else:
            print("└─ 🧅 Acompañante: 🚫 Ninguno")

        # Mostrar problemas
            if problemas or stock_bajo:
                print(f"\n🚫 PROBLEMAS IDENTIFICADOS:")
                for problema in problemas:
                    print(f"• {problema}")
                for bajo in stock_bajo:
                    print(f"• {bajo}")

        # Estado final
            if todos_ok:
                print(f"ESTADO: DISPONIBLE PARA VENTA")
                print(f"Puede proceder con la venta de {hotdog_seleccionado['nombre'].upper()}")
            else:
                print(f"ESTADO: NO DISPONIBLE PARA VENTA")

    #Funciones solo para agregar

    def seleccionar_salsas_interactivo(self):
        
        """Selecciona salsas de manera interactiva"""

        print(f"\n{'='*50}")
        print(f"🥫 SELECCIÓN DE SALSAS (Agregar múltiples)")
        print(f"{'='*50}")

        salsas_seleccionadas = []

        while True:
            print(f"Salsas actuales: {len(salsas_seleccionadas)}")
            if salsas_seleccionadas:
                print(f"Lista: {', '.join(salsas_seleccionadas)}")
            else:
                print(f"Lista: Vacía")

            print("\n¿Qué desea hacer?")
            print("1. Agregar más salsas")
            print("2. Finalizar selección de salsas")
            print("0. Cancelar registro completo")

            opcion = input("→ ")

            if opcion == "1":
                # Llamar a seleccionar_multiple para obtener nuevas salsas
                nuevas_salsas = self.seleccionar_multiple("Salsa")

                if nuevas_salsas is None:  # Usuario canceló
                    return None

                # Agregar las nuevas salsas evitando duplicados
                agregadas = 0
                i = 0
                while i < len(nuevas_salsas):
                    salsa = nuevas_salsas[i]
                    if salsa not in salsas_seleccionadas:
                        salsas_seleccionadas.append(salsa)
                        agregadas += 1
                    i += 1

                if agregadas > 0:
                    print(f"{agregadas} salsas agregadas exitosamente")
                else:
                    print("No se agregaron salsas nuevas (posibles duplicados)")

            elif opcion == "2":
                print(f"Selección de salsas finalizada")
                print(f"Total: {len(salsas_seleccionadas)} salsas")
                if salsas_seleccionadas:
                    print(f"Lista final: {', '.join(salsas_seleccionadas)}")
                return salsas_seleccionadas

            elif opcion == "0":
                print("Registro cancelado")
                return None

            else:
                print("Opción no válida")

    def seleccion_ingrediente(self,categoria):
        
        """Selecciona un ingrediente de una categoría específica"""

        print(f"\n{'='*50}")
        print(f"SELECCIÓN DE {categoria.upper()}")
        print(f"{'='*50}")
    
        # Buscar la categoría en los ingredientes
        categoria_data = None
        for cat in ingredientes:
            if cat["Categoria"] == categoria:
                categoria_data = cat
                break
    
        if not categoria_data:
            print(f"No se encontró la categoría: {categoria}")
            return None
        
        # Mostrar opciones disponibles
        print(f"Opciones de {categoria}:")
        opciones = categoria_data["Opciones"]

        for i in range(opciones.__len__()):
            nombre = opciones[i]["nombre"]
            stock = inventario.get(nombre, 0)
    

            # Información adicional según la categoría
            info_extra = ""
            if categoria == "Pan" or categoria == "Salchicha":
                if "tipo" in opciones[i] and "tamaño" in opciones[i]:
                    info_extra = f" ({opciones[i]['tipo']}, {opciones[i]['tamaño']} {opciones[i].get('unidad', '')})"
            elif categoria == "Salsa":
                if "base" in opciones[i]:
                    info_extra = f" (Base: {opciones[i]['base']})"
            elif categoria == "toppings":
                if "tipo" in opciones[i] and "presentación" in opciones[i]:
                    info_extra = f" ({opciones[i]['tipo']}, {opciones[i]['presentación']})"

            # Mostrar stock
            if stock == 0:
                stock_info = " - Stock: 0 ❌"
            elif stock <= 3:
                stock_info = f" - Stock: {stock} ⚠️"
            else:
                stock_info = f" - Stock: {stock} ✅"

            print(f"{i+1}. {nombre}{info_extra}{stock_info}")
    
        print("0. Cancelar registro")    
        # Solicitar selección
        while True:
            try:
                seleccion = int(input(f"\nSeleccione una opción (1-{len(opciones)}): "))

                if seleccion == 0:
                    print("Registro cancelado")
                    return None

                if 1 <= seleccion <= len(opciones):
                    ingrediente_seleccionado = opciones[seleccion-1]["nombre"]

                    # Verificar stock
                    stock_actual = inventario.get(ingrediente_seleccionado, 0)
                    if stock_actual == 0:
                        print(f"ADVERTENCIA: {ingrediente_seleccionado} no tiene stock disponible")
                        print("¿Desea continuar de todas formas?")
                        print("1. Sí, continuar")
                        print("2. No, seleccionar otro")

                        opcion_stock = input("→ ")
                        if opcion_stock != "1":
                            continue  # Volver a mostrar el menú
                        
                    return ingrediente_seleccionado
                else:
                    print(f"Opción no válida. Seleccione entre 1 y {len(opciones)}")

            except ValueError:
                print("Ingrese un número válido")

    def validar_tamanos(self, pan_nombre, salchicha_nombre):
    
        """Valida los tamaños del pan y la salchicha"""
    
    # Buscar información del pan
        pan_info = None
        for categoria in ingredientes:
            if categoria["Categoria"] == "Pan":
                for opcion in categoria["Opciones"]:
                    if opcion["nombre"] == pan_nombre:
                        pan_info = opcion
                        break
                    
        # Buscar información de la salchicha
        salchicha_info = None
        for categoria in ingredientes:
            if categoria["Categoria"] == "Salchicha":
                for opcion in categoria["Opciones"]:
                    if opcion["nombre"] == salchicha_nombre:
                        salchicha_info = opcion
                        break
                    
        if not pan_info or not salchicha_info:
            print("Error: No se pudo encontrar información de los ingredientes")
            return False

        tamano_pan = pan_info.get("tamaño", 0)
        tamano_salchicha = salchicha_info.get("tamaño", 0)

        # Si tienen el mismo tamaño, todo OK
        if tamano_pan == tamano_salchicha:
            return True

        # Si son diferentes, mostrar advertencia
        print(f"ADVERTENCIA: INCONSISTENCIA DE TAMAÑOS")
        print(f"{'='*50}")
        print(f"• Pan seleccionado: {pan_nombre} ({tamano_pan} pulgadas)")
        print(f"• Salchicha seleccionada: {salchicha_nombre} ({tamano_salchicha} pulgadas)")

        if tamano_salchicha < tamano_pan:
            print("La salchicha es más corta que el pan seleccionado.")
        else:
            print("La salchicha es más larga que el pan seleccionado.")

        print("\n¿Desea continuar así?")
        print("1. Sí, es mi intención")
        print("2. No, quiero cambiar la salchicha")
        print("3. No, quiero cambiar el pan")
        print("4. Cancelar registro completo")

        while True:
            opcion = input("→ ")

            if opcion == "1":
                return True
            elif opcion == "2":
                nueva_salchicha = self.seleccion_ingrediente("Salchicha")
                if nueva_salchicha:
                    return self.validar_tamanos(pan_nombre, nueva_salchicha)
                else:
                    return False
            elif opcion == "3":
                nuevo_pan = self.seleccion_ingrediente("Pan")
                if nuevo_pan:
                    return self.validar_tamanos(nuevo_pan, salchicha_nombre)
                else:
                    return False
            elif opcion == "4":
                print("Registro cancelado")
                return False
            else:
                print("Opción no válida")

    def verificar_advertencias(self, pan, salchicha, toppings_list, salsas, acompanante):
        
        """Verifica advertencias para los ingredientes seleccionados"""

        advertencias = []

        # Verificar stock de pan
        stock_pan = inventario.get(pan, 0)
        if stock_pan == 0:
            advertencias.append(f"Sin stock de pan '{pan}' (0 unidades)")
        elif stock_pan <= 3:
            advertencias.append(f"Stock bajo de pan '{pan}' (solo {stock_pan} unidades)")

        # Verificar stock de salchicha
        stock_salchicha = inventario.get(salchicha, 0)
        if stock_salchicha == 0:
            advertencias.append(f"Sin stock de salchicha '{salchicha}' (0 unidades)")
        elif stock_salchicha <= 3:
            advertencias.append(f"Stock bajo de salchicha '{salchicha}' (solo {stock_salchicha} unidades)")

        # Verificar stock de toppings
        for topping in toppings_list:
            stock_topping = inventario.get(topping, 0)
            if stock_topping == 0:
                advertencias.append(f"Sin stock de topping '{topping}' (0 unidades)")
            elif stock_topping <= 2:
                advertencias.append(f"Stock bajo de topping '{topping}' (solo {stock_topping} unidades)")

        # Verificar stock de salsas
        for salsa in salsas:
            stock_salsa = inventario.get(salsa, 0)
            if stock_salsa == 0:
                advertencias.append(f"Sin stock de salsa '{salsa}' (0 unidades)")
            elif stock_salsa <= 3:
                advertencias.append(f"Stock bajo de salsa '{salsa}' (solo {stock_salsa} unidades)")

        # Verificar stock de acompañante
        if acompanante:
            stock_acompanante = inventario.get(acompanante, 0)
            if stock_acompanante == 0:
                advertencias.append(f"Sin stock de acompañante '{acompanante}' (0 unidades)")
            elif stock_acompanante <= 3:
                advertencias.append(f"Stock bajo de acompañante '{acompanante}' (solo {stock_acompanante} unidades)")

        return advertencias
    
    def seleccionar_multiple(self, categoria):
        
        """Permite seleccionar múltiples opciones de una categoría"""

        print(f"\n{'='*50}")
        print(f"SELECCIÓN DE {categoria.upper()} (Múltiple)")
        print(f"{'='*50}")

        # Buscar la categoría
        categoria_data = None
        i = 0
        while i < len(ingredientes):
            if ingredientes[i]["Categoria"] == categoria:
                categoria_data = ingredientes[i]
                break
            i += 1

        if not categoria_data:
            print(f"No se encontró la categoría: {categoria}")
            return None

        # Mostrar opciones
        print(f"Opciones de {categoria} (puede elegir varios):")
        opciones = categoria_data["Opciones"]

        j = 0
        while j < len(opciones):
            nombre = opciones[j]["nombre"]
            stock = inventario.get(nombre, 0)

            # Información adicional
            info_extra = ""
            if categoria == "Salsa" and "base" in opciones[j]:
                info_extra = f" (Base: {opciones[j]['base']})"
            elif categoria == "toppings" and "tipo" in opciones[j]:
                info_extra = f" ({opciones[j]['tipo']})"

            # Mostrar stock
            if stock == 0:
                stock_info = " - Stock: 0 ❌"
            else:
                stock_info = f" - Stock: {stock} ✅"

            print(f"{j+1}. {nombre}{info_extra}{stock_info}")
            j += 1

        print("0. No agregar")
        print("00. Cancelar registro")

        # Solicitar selección múltiple
        while True:
            seleccion_str = input(f"\nIngrese números separados por coma (ej: 1,3,5): ").strip()

            if seleccion_str == "0":
                return []  # Lista vacía

            if seleccion_str == "00":
                return None  # Cancelación completa

            # Procesar múltiples selecciones
            partes = seleccion_str.split(",")
            numeros_validos = []
            k = 0

            while k < len(partes):
                num_str = partes[k].strip()
                if num_str:
                    try:
                        numero = int(num_str)
                        if 1 <= numero <= len(opciones):
                            numeros_validos.append(numero)
                        else:
                            print(f"Número {numero} fuera de rango (1-{len(opciones)})")
                    except ValueError:
                        print(f"'{num_str}' no es un número válido")
                k += 1

            if not numeros_validos:
                print("No seleccionó ninguna opción válida")
                continue
            
            # Obtener ingredientes seleccionados
            ingredientes_seleccionados = []
            m = 0
            while m < len(numeros_validos):
                nombre_ing = opciones[numeros_validos[m]-1]["nombre"]
                ingredientes_seleccionados.append(nombre_ing)
                m += 1

            return ingredientes_seleccionados

    def seleccionar_acompanante(self):
        
        """Selecciona un acompañante"""
    
        print(f"\n{'='*50}")
        print("🧅 ACOMPAÑANTE (Opcional)")
        print(f"{'='*50}")

        print("¿Desea agregar un acompañante?")
        print("1. Sí, agregar acompañante")
        print("2. No, continuar sin acompañante")
        print("0. Cancelar registro")

        while True:
            opcion = input("→ ")

            if opcion == "1":
                return self.seleccion_ingrediente("Acompañante")
            elif opcion == "2":
                return ""  # Sin acompañante
            elif opcion == "0":
                print("Registro cancelado")
                return None
            else:
                print("Opción no válida")

    def modificar_ingredientes(self, nombre, pan, salchicha, toppings, salsas, acompanante):
        
        """ Modifica los ingredientes de un hotdog"""
        
        print(f"\n{'='*50}")
        print("MODIFICAR INGREDIENTES")
        print(f"{'='*50}")

        # Guardar valores actuales
        pan_actual = pan
        salchicha_actual = salchicha
        toppings_actual = toppings.copy() if toppings else []
        salsas_actual = salsas.copy() if salsas else []
        acompanante_actual = acompanante

        while True:
            print(f"\n¿Qué ingrediente desea modificar?")
            print("1. Pan")
            print("2. Salchicha")
            print("3. Toppings (modificar específicos)")
            print("4. Salsas (modificar específicas)")
            print("5. Acompañante")
            print("6.Finalizar todas las modificaciones")
            print("0.Cancelar registro completo")

            opcion = input("→ ")

            if opcion == "1":
                nuevo_pan = self.seleccion_ingrediente("Pan")
                if nuevo_pan and self.validar_tamanos(nuevo_pan, salchicha_actual):
                    pan_actual = nuevo_pan
                    print(f"Pan cambiado a: {nuevo_pan}")

            elif opcion == "2":
                nueva_salchicha = self.seleccion_ingrediente("Salchicha")
                if nueva_salchicha and self.validar_tamanos(pan_actual, nueva_salchicha):
                    salchicha_actual = nueva_salchicha
                    print(f"Salchicha cambiada a: {nueva_salchicha}")

            elif opcion == "3":
                # MODIFICACIÓN ESPECÍFICA DE TOPPINGS
                resultado_toppings = self.modificar_toppings(toppings_actual)
                if resultado_toppings is None:
                    return None, None, None, None, None
                toppings_actual = resultado_toppings

            elif opcion == "4":
                # MODIFICACIÓN ESPECÍFICA DE SALSAS
                resultado_salsas = self.modificar_salsas(salsas_actual)
                if resultado_salsas is None:
                    return None, None, None, None, None
                salsas_actual = resultado_salsas

            elif opcion == "5":
                nuevo_acompanante = self.seleccionar_acompanante()
                if nuevo_acompanante is not None:
                    acompanante_actual = nuevo_acompanante
                    if acompanante_actual:
                        print(f"Acompañante cambiado a: {acompanante_actual}")
                    else:
                        print("Acompañante removido")

            elif opcion == "6":
                return pan_actual, salchicha_actual, toppings_actual, salsas_actual, acompanante_actual

            elif opcion == "0":
                print("Registro cancelado")
                return None, None, None, None, None

            else:
                print("Opción no válida")
    
    def seleccionar_toppings_interactivo(self):
        
        """Selecciona toppings de manera interactiva"""

        print(f"\n{'='*50}")
        print(f"🍟 SELECCIÓN DE TOPPINGS (Agregar múltiples)")
        print(f"{'='*50}")
        
        toppings_seleccionados = []
        
        while True:
            print(f"\n📋 Toppings actuales: {len(toppings_seleccionados)}")
            if toppings_seleccionados:
                print(f"📝 Lista: {', '.join(toppings_seleccionados)}")
            else:
                print(f"📝 Lista: Vacía")
            
            print("\n¿Qué desea hacer?")
            print("1. Agregar más toppings")
            print("2. Finalizar selección de toppings")
            print("0. Cancelar registro completo")
            
            opcion = input("→ ")
            
            if opcion == "1":
                # Llamar a seleccionar_multiple para obtener nuevos toppings
                nuevos_toppings = self.seleccionar_multiple("toppings")
                
                if nuevos_toppings is None:  # Usuario canceló
                    return None
                
                # Agregar los nuevos toppings evitando duplicados
                agregados = 0
                i = 0
                while i < len(nuevos_toppings):
                    topping = nuevos_toppings[i]
                    if topping not in toppings_seleccionados:
                        toppings_seleccionados.append(topping)
                        agregados += 1
                    i += 1
                
                if agregados > 0:
                    print(f"{agregados} toppings agregados exitosamente")
                else:
                    print("No se agregaron toppings nuevos (posibles duplicados)")
                    print("Asegure que el topping que desea agregar sea uno que no este ya seleccionado")


            elif opcion == "2":
                print(f"Selección de toppings finalizada")
                print(f"Total: {len(toppings_seleccionados)} toppings")
                if toppings_seleccionados:
                    print(f"📝 Lista final: {', '.join(toppings_seleccionados)}")
                return toppings_seleccionados
                
            elif opcion == "0":
                print("Registro cancelado")
                return None
                
            else:
                print("Opción no válida")
            
    def mostrar_resumen_y_confirmar(self, nombre, pan, salchicha, toppings, salsas, acompanante):
        
        """Muestra un resumen del pedido y solicita confirmación"""
        
        print(f"\n{'='*60}")
        print("RESUMEN DEL NUEVO HOT DOG")
        print(f"{'='*60}")

        # Mostrar información básica
        print(f"🌭 NOMBRE: {nombre}")
        print(f"🥖 PAN: {pan} {self.obtener_detalle_ingrediente('Pan', pan)}")
        print(f"🌭 SALCHICHA: {salchicha} {self.obtener_detalle_ingrediente('Salchicha', salchicha)}")

        # Mostrar toppings
        if toppings:
            print(f"🍟 TOPPINGS: {', '.join(toppings)}")
        else:
            print(f"🍟 TOPPINGS: 🚫 Ninguno")

        # Mostrar salsas
        if salsas:
            print(f"🥫 SALSAS: {', '.join(salsas)}")
        else:
            print(f"🥫 SALSAS: 🚫 Ninguna")

        # Mostrar acompañante
        if acompanante:
            print(f"🧅 ACOMPAÑANTE: {acompanante} {self.obtener_detalle_ingrediente('Acompañante', acompanante)}")
        else:
            print(f"🧅 ACOMPAÑANTE: 🚫 Ninguno")

        # Verificar advertencias
        advertencias = self.verificar_advertencias(pan, salchicha, toppings, salsas, acompanante)
        if advertencias:
            print(f"ADVERTENCIAS:")
            i = 0
            while i < len(advertencias) and i < 3:  # Mostrar máximo 3
                print(f"• {advertencias[i]}")
                i += 1
            if len(advertencias) > 3:
                print(f"• ... y {len(advertencias) - 3} más")
        else:
            print(f"Todos los ingredientes existen en el sistema")

        print(f"\n{'='*60}")
        print("¿Confirmar la creación de este hot dog?")
        print("1. Sí, crear hot dog")
        print("2. No, modificar ingredientes")
        print("3. Cancelar y volver al menú")

        while True:
            opcion = input("→ ")

            if opcion == "1":
                return True, pan, salchicha, toppings, salsas, acompanante

            elif opcion == "2":
                resultado = self.modificar_ingredientes(nombre, pan, salchicha, toppings, salsas, acompanante)
                if resultado[0] is None:
                    return False, None, None, None, None, None
                else:
                    pan, salchicha, toppings, salsas, acompanante = resultado
                    return self.mostrar_resumen_y_confirmar(nombre, pan, salchicha, toppings, salsas, acompanante)

            elif opcion == "3":
                print("Registro cancelado")
                return False, None, None, None, None, None

            else:
                print("Opción no válida")

    def obtener_detalle_ingrediente(self, categoria, nombre_ingrediente):
        
        """Obtiene detalles de un ingrediente específico"""

        #Aunque parezca igual a la funcion obtener_info_ingrediente, 
        #esta funcion te lo da de forma más detallada


        if not nombre_ingrediente:
            return ""

        for cat in ingredientes:
            if cat["Categoria"] == categoria:
                for opcion in cat["Opciones"]:
                    if opcion["nombre"] == nombre_ingrediente:
                        if categoria == "Salsa":
                            return f"(Base: {opcion['base']})"
                        elif categoria in ["Pan", "Salchicha"]:
                            if "tipo" in opcion and "tamaño" in opcion:
                                return f"({opcion['tipo']}, {opcion['tamaño']} {opcion.get('unidad', '')})"
                        elif categoria == "Acompañante":
                            if "tipo" in opcion and "tamaño" in opcion:
                                unidad = opcion.get('unidad', '')
                                if unidad == 'gramos':
                                    return f"({opcion['tipo']}, {opcion['tamaño']}g)"
                                elif unidad == 'mililitros':
                                    return f"({opcion['tipo']}, {opcion['tamaño']}ml)"
                                else:
                                    return f"({opcion['tipo']}, {opcion['tamaño']} {unidad})"
                        elif categoria == "toppings":
                            if "tipo" in opcion:
                                return f"({opcion['tipo']})"

        return ""
    
    
    def modificar_toppings(self, toppings_actuales):
        
        """Modifica los toppings actuales"""
        
    

        print(f"\n{'='*50}")
        print(f"🍟 MODIFICAR TOPPINGS")
        print(f"{'='*50}")

        toppings = toppings_actuales.copy() if toppings_actuales else []

        while True:
            print(f"\n📋 Toppings actuales: {len(toppings)}")
            if toppings:
                # Mostrar toppings numerados
                i = 0
                while i < len(toppings):
                    print(f"  {i+1}. {toppings[i]}")
                    i += 1
            else:
                print("No hay toppings")

            print("\n¿Qué desea hacer?")
            print("1. Agregar nuevos toppings")
            print("2. Eliminar un topping")
            print("3. Reemplazar todos los toppings")
            print("4. Finalizar modificación de toppings")
            print("0. Cancelar todo el registro")

            opcion = input("→ ")

            if opcion == "1":
                # Agregar nuevos toppings
                nuevos_toppings = self.seleccionar_multiple("toppings")
                if nuevos_toppings is None:
                    return None

                if nuevos_toppings:
                    # Agregar evitando duplicados
                    agregados = 0
                    j = 0
                    while j < len(nuevos_toppings):
                        topping = nuevos_toppings[j]
                        if topping not in toppings:
                            toppings.append(topping)
                            agregados += 1
                        j += 1

                    if agregados > 0:
                        print(f"{agregados} toppings agregados")
                    else:
                        
                        print("No se agregaron toppings nuevos")
                        

            elif opcion == "2":
                # Eliminar un topping
                if not toppings:
                    print("No hay toppings para eliminar")
                    continue
                
                print("\n¿Qué topping desea eliminar?")
                k = 0
                while k < len(toppings):
                    print(f"  {k+1}. {toppings[k]}")
                    k += 1
                print("  0. Volver")

                try:
                    seleccion = int(input("→ "))
                    if seleccion == 0:
                        continue
                    if 1 <= seleccion <= len(toppings):
                        topping_eliminado = toppings.pop(seleccion-1)
                        print(f"Topping '{topping_eliminado}' eliminado")
                    else:
                        print("Opción no válida")
                except ValueError:
                    print("Ingrese un número válido")

            elif opcion == "3":
                # Reemplazar todos los toppings
                nuevos_toppings = self.seleccionar_multiple("toppings")
                if nuevos_toppings is None:
                    return None
                toppings = nuevos_toppings
                print("Todos los toppings han sido reemplazados")

            elif opcion == "4":
                return toppings

            elif opcion == "0":
                print("Registro cancelado")
                return None

            else:
                print("Opción no válida")
    
    def modificar_salsas(self, salsas_actuales):
        
        """Modifica las salsas actuales"""
        
        print(f"\n{'='*50}")
        print(f"🥫 MODIFICAR SALSAS")
        print(f"{'='*50}")

        salsas = salsas_actuales.copy() if salsas_actuales else []

        while True:
            print(f"\n📋 Salsas actuales: {len(salsas)}")
            if salsas:
                # Mostrar salsas numeradas
                i = 0
                while i < len(salsas):
                    print(f"  {i+1}. {salsas[i]}")
                    i += 1
            else:
                print("No hay salsas")

            print("\n¿Qué desea hacer?")
            print("1. Agregar nuevas salsas")
            print("2. Eliminar una salsa")
            print("3. Reemplazar todas las salsas")
            print("4. Finalizar modificación de salsas")
            print("0. Cancelar todo el registro")

            opcion = input("→ ")

            if opcion == "1":
                # Agregar nuevas salsas
                nuevas_salsas = self.seleccionar_multiple("Salsa")
                if nuevas_salsas is None:
                    return None

                if nuevas_salsas:
                    # Agregar evitando duplicados
                    agregadas = 0
                    j = 0
                    while j < len(nuevas_salsas):
                        salsa = nuevas_salsas[j]
                        if salsa not in salsas:
                            salsas.append(salsa)
                            agregadas += 1
                        j += 1

                    if agregadas > 0:
                        print(f"{agregadas} salsas agregadas")
                    else:
                        print("No se agregaron salsas nuevas")
                        print("Asegure que el topping que desea agregar sea uno que no este ya seleccionado")

            elif opcion == "2":
                # Eliminar una salsa
                if not salsas:
                    print("No hay salsas para eliminar")
                    continue
                
                print("\n¿Qué salsa desea eliminar?")
                k = 0
                while k < len(salsas):
                    print(f"  {k+1}. {salsas[k]}")
                    k += 1
                print("  0. Volver")

                try:
                    seleccion = int(input("→ "))
                    if seleccion == 0:
                        continue
                    if 1 <= seleccion <= len(salsas):
                        salsa_eliminada = salsas.pop(seleccion-1)
                        print(f"Salsa '{salsa_eliminada}' eliminada")
                    else:
                        print("Opción no válida")
                except ValueError:
                    print("Ingrese un número válido")

            elif opcion == "3":
                # Reemplazar todas las salsas
                nuevas_salsas = self.seleccionar_multiple("Salsa")
                if nuevas_salsas is None:
                    return None
                salsas = nuevas_salsas
                print("Todas las salsas han sido reemplazadas")

            elif opcion == "4":
                return salsas

            elif opcion == "0":
                print("Registro cancelado")
                return None

            else:
                print("Opción no válida")
    
    
    def agregar(self):
        
        """grega un hotdog personalizado al menú"""

        print("\n🌭 AGREGAR NUEVO HOT DOG AL MENÚ")
        print("=" * 50)

        #  Nombre
        nombre = input("Ingrese un nombre único para el nuevo hot dog: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío")
            return

        #  Pan
        pan = self.seleccion_ingrediente("Pan")
        if not pan:
            return

        #  Salchicha
        salchicha = self.seleccion_ingrediente("Salchicha")
        if not salchicha:
            return

        # Validar tamaños
        if not self.validar_tamanos(pan, salchicha):
            return

        # Toppings (simplificado)
        toppings = self.seleccionar_toppings_interactivo()
        if toppings is None:
            return

        #  Salsas
        salsas = self.seleccionar_salsas_interactivo()
        if salsas is None:
            return

        #  Acompañante
        acompanante = self.seleccionar_acompanante()
        if acompanante is None:
            return

        # Mostrar resumen y confirmar
        resultado = self.mostrar_resumen_y_confirmar(nombre, pan, salchicha, toppings, salsas, acompanante)
        confirmado, pan_final, salchicha_final, toppings_final, salsas_final, acompanante_final = resultado

        if confirmado:
            nuevo_hotdog = {
                "nombre": nombre,
                "Pan": pan_final,
                "Salchicha": salchicha_final,
                "toppings": toppings_final,
                "salsas": salsas_final,
                "Acompañante": acompanante_final
            }
            self.menu.append(nuevo_hotdog)
            print(f"'{nombre}' ha sido agregado al menú correctamente!")
            input("Presione Enter para continuar...")
    
    #Funciones de eliminar
    def mostrar_lista_hotdogs(self):
        
        """Muestra la lista de hotdogs disponibles"""
    
        print("\n📋 HOT DOGS EN EL MENÚ:")
        i = 0
        while i < len(hotdog_seleccionado):
            hotdog = hotdog_seleccionado[i]
            emoji = self.obtener_emoji(hotdog['nombre'])
            print(f"{i+1}. {hotdog['nombre'].upper()} {emoji}")

            # Mostrar información básica
            print(f"   🥖 Pan: {hotdog['Pan']}")
            print(f"   🌭 Salchicha: {hotdog['Salchicha']}")

            # Mostrar toppings
            toppings = hotdog.get('toppings', [])
            if toppings:
                print(f"   🍟 Toppings: {len(toppings)}")
            else:
                print(f"   🍟 Toppings: Ninguno")

            # Mostrar salsas
            salsas = hotdog.get('salsas', [])
            if salsas:
                print(f"   🥫 Salsas: {len(salsas)}")
            else:
                print(f"   🥫 Salsas: Ninguna")

            # Mostrar acompañante
            acompanante = hotdog.get('Acompañante')
            if acompanante:
                print(f"   🧅 Acompañante: {acompanante}")
            else:
                print(f"   🧅 Acompañante: Ninguno")

            print()  # Línea en blanco
            i += 1

    def procesar_eliminacion(self, hotdog_seleccionado):
        
        """Procesa la eliminación de un hotdog"""
       
        
        nombre = hotdog_seleccionado['nombre']

        # Verificar si el hot dog tiene inventario suficiente
        tiene_inventario, problemas = self.verificar_inventario_hotdog(hotdog_seleccionado)

        print(f"\n{'='*60}")

        if tiene_inventario:
            # Hot dog con inventario - requiere confirmación
            print(f"ELIMINAR HOT DOG CON INVENTARIO DISPONIBLE")
            print(f"{'='*60}")
            print(f"🌭 HOT DOG: {nombre.upper()} {self.obtener_emoji(nombre)}")
            print(f"Estado: ✅ DISPONIBLE PARA VENTA")

            print(f"\n📋 INGREDIENTES DISPONIBLES:")
            print(f"• 🥖 Pan: {hotdog_seleccionado['Pan']} ✅")
            print(f"• 🌭 Salchicha: {hotdog_seleccionado['Salchicha']} ✅")

            toppings = hotdog_seleccionado.get('toppings', [])
            if toppings:
                print(f"• 🍟 Toppings: {len(toppings)} disponibles ✅")

            salsas = hotdog_seleccionado.get('salsas', [])
            if salsas:
                print(f"• 🥫 Salsas: {len(salsas)} disponibles ✅")

            if hotdog_seleccionado.get('Acompañante'):
                print(f"• 🧅 Acompañante: {hotdog_seleccionado['Acompañante']} ✅")

            print(f"\n🚨 ADVERTENCIA: Este hot dog tiene inventario suficiente")
            print(f"    para continuar vendiéndose.")

        else:
            # Hot dog sin inventario completo
            print(f"✅ ELIMINAR HOT DOG SIN INVENTARIO COMPLETO")
            print(f"{'='*60}")
            print(f"🌭 HOT DOG: {nombre.upper()} {self.obtener_emoji(nombre)}")
            print(f"Estado: NO DISPONIBLE PARA VENTA")

            print(f"\n📋 PROBLEMAS DE INVENTARIO:")
            j = 0
            while j < len(problemas) and j < 5:  # Mostrar máximo 5 problemas
                print(f"• {problemas[j]}")
                j += 1

            if len(problemas) > 5:
                print(f"• ... y {len(problemas) - 5} más")

        # Solicitar confirmación
        self.solicitar_confirmacion_eliminacion(hotdog_seleccionado, tiene_inventario)

    def verificar_inventario_hotdog(self, hotdog):
        
        """Verifica el inventario del hotdog"""
        
        problemas = []

        # Verificar pan
        pan_stock = inventario.get(hotdog["Pan"], 0)
        if pan_stock == 0:
            problemas.append(f"Sin stock de pan: {hotdog['Pan']}")

        # Verificar salchicha
        salchicha_stock = inventario.get(hotdog["Salchicha"], 0)
        if salchicha_stock == 0:
            problemas.append(f"Sin stock de salchicha: {hotdog['Salchicha']}")

        # Verificar toppings
        toppings = hotdog.get('toppings', [])
        k = 0
        while k < len(toppings):
            topping_stock = inventario.get(toppings[k], 0)
            if topping_stock == 0:
                problemas.append(f"Sin stock de topping: {toppings[k]}")
            k += 1

        # Verificar salsas
        salsas = hotdog.get('salsas', [])
        m = 0
        while m < len(salsas):
            salsa_stock = inventario.get(salsas[m], 0)
            if salsa_stock == 0:
                problemas.append(f"Sin stock de salsa: {salsas[m]}")
            m += 1

        # Verificar acompañante
        acompanante = hotdog.get('Acompañante')
        if acompanante:
            acompanante_stock = inventario.get(acompanante, 0)
            if acompanante_stock == 0:
                problemas.append(f"Sin stock de acompañante: {acompanante}")

        # Si no hay problemas, tiene inventario completo
        tiene_inventario = (len(problemas) == 0)

        return tiene_inventario, problemas

    def solicitar_confirmacion_eliminacion(self, hotdog, tiene_inventario):
        
        """Solicita confirmación para eliminar"""

        nombre = hotdog['nombre']

        print(f"\n¿Está seguro que desea eliminar \"{nombre}\" del menú?")
        print("1. Sí, eliminar")
        print("2. No, mantener en el menú")

        if tiene_inventario:
            print("3. Ver detalles de inventario completo")

        print("0. Cancelar")

        while True:
            try:
                opcion = int(input("→ "))

                if opcion == 1:
                    self.ejecutar_eliminacion(hotdog, tiene_inventario)
                    break
                elif opcion == 2:
                    print(f"\"{nombre}\" se mantiene en el menú")
                    input("Presione Enter para continuar...")
                    break
                elif opcion == 3 and tiene_inventario:
                    self.mostrar_detalle_inventario_completo(hotdog)
                    # Volver a preguntar después de mostrar detalles
                    print(f"\n¿Eliminar \"{nombre}\" del menú?")
                    print("1. Sí, eliminar")
                    print("2. No, mantener")
                    print("0. Cancelar")
                elif opcion == 0:
                    break
                else:
                    print("Opción no válida")

            except ValueError:
                print("Ingrese un número válido")

    def ejecutar_eliminacion(self, hotdog, tiene_inventario):
        
        """Ejecuta la eliminación del hotdog"""

        nombre = hotdog['nombre']

        # Remover del menú
        self.menu.remove(hotdog)

        print(f"HOT DOG ELIMINADO EXITOSAMENTE")
        print(f"{'='*50}")
        print(f"\"{nombre}\" ha sido removido del menú.")
        print(f"Impacto:")
        print(f"• Hot dogs en menú: {len(self.menu)}")
        print(f"• El hot dog ya no estará disponible para venta")

        # Mensaje contextual según el inventario
        if tiene_inventario:
            print(f"Hot dog eliminado por solicitud del usuario.")
            print(f"   Stock suficiente estaba disponible.")
        else:
            print(f"Hot dog eliminado por falta de inventario.")
            print(f"   Considere reabastecer ingredientes si desea volver a ofrecerlo.")

        input("\nPresione Enter para continuar...")

    def mostrar_detalle_inventario_completo(self, hotdog):
        
        """Muestra el detalle completo del inventario"""

        nombre = hotdog['nombre']

        print(f"DETALLE DE INVENTARIO - {nombre.upper()}")
        print(f"{'='*60}")

        # Pan
        pan_stock = inventario.get(hotdog["Pan"], 0)
        print(f"🥖 PAN: {hotdog['Pan']}")
        print(f"   • Stock: {pan_stock} unidades")
        print(f"   • Estado: {'✅ SUFICIENTE' if pan_stock > 0 else '❌ FALTANTE'}")

        # Salchicha
        salchicha_stock = inventario.get(hotdog["Salchicha"], 0)
        print(f"\n🌭 SALCHICHA: {hotdog['Salchicha']}")
        print(f"   • Stock: {salchicha_stock} unidades")
        print(f"   • Estado: {'✅ SUFICIENTE' if salchicha_stock > 0 else '❌ FALTANTE'}")

        # Toppings
        toppings = hotdog.get('toppings', [])
        if toppings:
            print(f"\n🍟 TOPPINGS:")
            t = 0
            while t < len(toppings):
                topping_stock = inventario.get(toppings[t], 0)
                estado = "✅" if topping_stock > 0 else "❌"
                print(f"   • {toppings[t]}: {topping_stock} unidades {estado}")
                t += 1

        # Salsas
        salsas = hotdog.get('salsas', [])
        if salsas:
            print(f"\n🥫 SALSAS:")
            s = 0
            while s < len(salsas):
                salsa_stock = inventario.get(salsas[s], 0)
                estado = "✅" if salsa_stock > 0 else "❌"
                print(f"   • {salsas[s]}: {salsa_stock} unidades {estado}")
                s += 1

        # Acompañante
        acompanante = hotdog.get('Acompañante')
        if acompanante:
            acompanante_stock = inventario.get(acompanante, 0)
            print(f"\n🧅 ACOMPAÑANTE: {acompanante}")
            print(f"   • Stock: {acompanante_stock} unidades")
            print(f"   • Estado: {'✅ SUFICIENTE' if acompanante_stock > 0 else '❌ FALTANTE'}")

    def eliminar(self):
        
        """Elimina un hot dog del menú con validaciones"""

        print("ELIMINAR HOT DOG DEL MENÚ")
        print("=" * 50)

        # Verificar si hay hot dogs en el menú
        if not self.menu:
            print("No hay hot dogs en el menú")
            input("Presione Enter para continuar...")
            return

        # Mostrar lista de hot dogs
        self.mostrar_lista_hotdogs()

        try:
            opcion = int(input("\nSeleccione el hot dog a eliminar (0 para cancelar): "))
            if opcion == 0:
                return

            
        
            if 1 <= opcion <= len(self.menu):
                hotdog_seleccionado = self.menu[opcion-1]
                self.procesar_eliminacion(hotdog_seleccionado)
            else:
                print("Opción no válida")
                input("Presione Enter para continuar...")

        except ValueError:
            print("Ingrese un número válido")
            input("Presione Enter para continuar...")

def iniciar_programa_GestorMenu(ingredientes_data, menu_data):
    # Creamos esta funcion que se usara en main.py
    gestor = GestorMenu(ingredientes_data, menu_data)
        
        # Bucle del menú de gestión
    while True:
        print("\n--- MENÚ DE GESTIÓN DEL MENÚ ---")
        print("1. Listar el menu")
        print("2. Ver hotdog especifico")
        print("3. Agregar nuevo item al menu")
        print("4. Eliminar item del menu")
        print("5. Volver al menú principal")
            
        opcion = input("Seleccione una opción: ")
            
        if opcion == '1':
            gestor.ver_lista(hotdog_seleccionado)
            t.sleep(1)
        elif opcion == '2':
            gestor.ver_hotdog_espesifico(hotdog_seleccionado)
            t.sleep(1)
        elif opcion == '3':
            gestor.agregar()
            t.sleep(1)
        elif opcion == '4':
            gestor.eliminar()
            t.sleep(1)
        elif opcion == '5':
            try:
                guardar_todo(menu_data,ingredientes_data, inventario)
            except Exception as e:
                print(f"¡ERROR CRÍTICO AL INTENTAR GUARDAR!: {e}")
                print("Los cambios podrían no ser permanentes.")

            print("Regresando al menú principal...")
            t.sleep(2)
            break 
        else:
            print("Opción no válida. Intente de nuevo.")

