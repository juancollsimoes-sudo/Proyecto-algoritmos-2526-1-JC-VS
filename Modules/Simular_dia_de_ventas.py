#Simular dia de ventas
import random as r
from collections import Counter # Útil para los reportes
import time as t
from Source.Gestion_archivos import guardar_todo

class SimuladorDia:
    
    def __init__(self, ingredientes_data, inventario_data, menu_data):
        self.ingredientes_data = ingredientes_data
        self.inventario_data = inventario_data
        self.menu_data = menu_data

        # obtener lista de acompañantes
        self.lista_acompanantes = self.obtener_lista_acompanantes()

        #se definen cuales clientes cambiaron de opinion, no compraron. cuantos hotdogs fueron vendidos y cuales acompañantes fueron vendidos
        self.clientes_cambio_opinion = 0
        self.clientes_no_compraron_stock = 0
        self.hotdogs_vendidos_total = 0
        self.acompanantes_vendidos_total = 0 
        
        # Usamos Counter para facilitar el conteo, lo que hace es contar cada uno de los objetos de una lista
        self.conteo_hotdogs_vendidos = Counter()
        self.fallos_por_hotdog = Counter()
        self.fallos_por_ingrediente = Counter()
        
        self.num_clientes_dia = 0


    def obtener_lista_acompanantes(self):
        #Extrae la lista de acompañantes de ingredientes
        try:
            cat_acompañante = next(cat for cat in self.ingredientes_data if cat['Categoria'] == 'Acompañante') #logra separar cada acompañante individualmente
            return cat_acompañante.get('Opciones', [])
        except StopIteration: # este except lo que hace es parar la iteracion de separar cada acompañante individualmente, ya que no encontro en ingredientes.json la categoria
            print("Advertencia: No se encontró categoría 'Acompañante'.")
            return []

    def _obtener_ingredientes_hotdog(self, hotdog_obj):
        #ayuda a obtener los ingredientes del hotdog
        try: # se intenta lo mismo que el anterior, se busca un hotdog en especifico buscando su pan y salchicha
            ingredientes_req = [
                hotdog_obj['Pan'],
                hotdog_obj['Salchicha']
            ]
            ingredientes_req.extend(hotdog_obj['toppings'])
            ingredientes_req.extend(hotdog_obj['salsas'])
            #estos dos extend lo que hace es que se den por separado los toppings y las salsas del hotdog de un hotdog en especifico
            return ingredientes_req
        except KeyError:
            # Esto pasa si el menu.json tiene un hotdog mal definido
            print(f"Error: El hotdog '{hotdog_obj.get('nombre', 'DESCONOCIDO')}' tiene una definición incorrecta.")
            return None


    def simular_dia(self):
        #se inicia la simulacion el dia:
        print("="*50)
        print("---INICIANDO SIMULACIÓN ---")
        print("="*50)
        
        # Generar número aleatorio de clientes 
        self.num_clientes_dia = r.randint(0, 200)
        print(f"Simulando el día con {self.num_clientes_dia} clientes")
        t.sleep(1)
        
        for i in range(1, self.num_clientes_dia + 1):
            #aca basicamente te dice que cada cliente va a poder comprar maximo de 5 hotdogs
            num_hotdogs_compra = r.randint(0, 5)
            if num_hotdogs_compra == 0:
                #si el cliente no compro nada significa que cambio de opinion
                print(f"El cliente {i} cambió de opinión")
                self.clientes_cambio_opinion += 1
                continue # Pasa al siguiente cliente

            # Si el cliente si quiere comprar 
            
            orden_cliente = [] # Lista de hotdogs y acompañantes de este cliente
            ingredientes_orden_completa = Counter() # Contador para todos los ingredientes
            for j in range(num_hotdogs_compra):
                # Seleccionar aleatoriamente un hot dog del menú
                hotdog_obj = r.choice(self.menu_data) 
                # Seleccionar aleatoriamente si compró un acompañante adicional
                acompanante_obj = None
                if r.choice([True, False]) and self.lista_acompanantes: # lo que hace esto es que haya un 50% de probabilidad de que compre o no un acompañante
                    acompanante_obj = r.choice(self.lista_acompanantes)
                
                # Guardamos la orden para procesarla
                orden_cliente.append( (hotdog_obj, acompanante_obj) )

                # Acumulamos los ingredientes necesarios para este hotdog
                ingredientes_de_1_hotdog = self._obtener_ingredientes_hotdog(hotdog_obj)
                if ingredientes_de_1_hotdog:
                    ingredientes_orden_completa.update(ingredientes_de_1_hotdog)
                
                # Acumulamos el acompañante 
                if acompanante_obj:
                    ingredientes_orden_completa.update([acompanante_obj['nombre']])

            # Revisar si hay suficiente inventario 
            # Verificamos la orden completa del cliente
            
            ingrediente_fallido = None
            for ingrediente, cantidad_necesaria in ingredientes_orden_completa.items():
                if self.inventario_data.get(ingrediente, 0) < cantidad_necesaria:
                    ingrediente_fallido = ingrediente
                    break # Si falta 1 ingrediente, falla toda la orden

            
            if ingrediente_fallido:
                self.clientes_no_compraron_stock += 1
                
                # Identificar qué hotdog causó el fallo
                hotdog_causante = "Varios"
                for hotdog_objeto, acompanante_objeto in orden_cliente:
                    ingredientes_hotdog = self._obtener_ingredientes_hotdog(hotdog_objeto) or []
                    ingredientes_acompanante = [acompanante_objeto['nombre']] if acompanante_objeto else []
                    
                    if ingrediente_fallido in ingredientes_hotdog or ingrediente_fallido in ingredientes_acompanante:
                        hotdog_causante = hotdog_objeto['nombre']
                        break 
                
                print(f"El cliente {i} se marchó sin llevarse nada.")
                print(f"No se pudo comprar '{hotdog_causante}' por falta de '{ingrediente_fallido}'.")
                
                # Actualizar reporte de fallos
                self.fallos_por_hotdog.update([hotdog_causante])
                self.fallos_por_ingrediente.update([ingrediente_fallido])
            else:
                # Imprimir la lista de hot dogs
                nombres_hotdogs = [hotdog['nombre'] for hotdog, acompanante in orden_cliente]
                print(f"El cliente {i} compró: {', '.join(nombres_hotdogs)}")

                # Restar del inventario
                for ingrediente, cantidad_a_restar in ingredientes_orden_completa.items():
                    self.inventario_data[ingrediente] -= cantidad_a_restar
                
                # Actualizar reporte de ventas exitosas
                self.hotdogs_vendidos_total += num_hotdogs_compra
                self.conteo_hotdogs_vendidos.update(nombres_hotdogs)
                
                # Contar acompañantes vendidos
                for hotdog, acompanante in orden_cliente:
                    if acompanante: # Si se vendió un acompañante adicional
                        self.acompanantes_vendidos_total += 1

        # Reporte Final del Día 
        print("\n" + "="*50)
        print("REPORTE FINAL DE SIMULACIÓN")
        print("="*50)

        # Cuál fue el total de clientes
        print(f"● Clientes totales: {self.num_clientes_dia}")
        
        # Cuántos clientes cambiaron de opinión
        print(f"● Clientes que cambiaron de opinión: {self.clientes_cambio_opinion}")
        
        # Cuántos clientes no pudieron comprar
        print(f"● Clientes que no pudieron comprar (por stock): {self.clientes_no_compraron_stock}")

        # Cuál fue el promedio de hot dogs por cliente
        promedio_hd = (self.hotdogs_vendidos_total / self.num_clientes_dia) if self.num_clientes_dia > 0 else 0
        print(f"● Promedio de hot dogs por cliente (total): {promedio_hd:.2f}")

        # Cuál fue el hot dog más vendido
        if self.conteo_hotdogs_vendidos:
            hotdog_mas_vendido, cantidad = self.conteo_hotdogs_vendidos.most_common(1)[0]
            print(f"● Hot dog más vendido: {hotdog_mas_vendido} ({cantidad} unidades)")
        else:
            print("● Hot dog más vendido: Ninguno")

        # Cuántos acompañantes fueron vendidos
        print(f"● Acompañantes (adicionales) vendidos: {self.acompanantes_vendidos_total}")

        print("\n--- Detalles de Fallos de Stock ---")
        
        # Cuáles fueron los hot dogs que causaron que el cliente se marchara
        print("● Hot dogs que causaron el fallo:")
        if not self.fallos_por_hotdog:
            print(" Ninguno (No hubo fallos de stock)")
        else:
            for hotdog, veces in self.fallos_por_hotdog.items():
                print(f"{hotdog}: {veces} veces")

        # Cuáles fueron los ingredientes que causaron que el cliente se marchara
        print("\n● Ingredientes que causaron el fallo:")
        if not self.fallos_por_ingrediente:
            print("Ninguno (No hubo fallos de stock)")
        else:
            for ingrediente, veces in self.fallos_por_ingrediente.items():
                print(f"{ingrediente}: {veces} veces")
        
        print("="*50)
        print("\nGuardando inventario actualizado post-simulación...")
        try:
            guardar_todo(self.ingredientes_data, self.menu_data, self.inventario_data)
            print("¡Simulación completada! 'inventario.json' ha sido actualizado.")
        except Exception as e:
            print(f" Error al guardar el inventario: {e}")

#funcion que se colocara en el Main

def iniciar_programa_Simulador(ingredientes_data, menu_data, inventario_data):
    
    # 1. Crear la instancia del simulador
    simulador = SimuladorDia(ingredientes_data, inventario_data, menu_data)
    
    # 2. Ejecutar la simulación
    simulador.simular_dia()
    
    print("\n...volviendo al menú principal.")
    t.sleep(3)
