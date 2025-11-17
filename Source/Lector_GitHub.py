#Programa hecho por Juan Coll y Valeria Solorzano

##Primera parte llamada a la API
#Empezamos con los imports, el request es para llamar a la API, el Json es para leer los archivos que contengan la repo, y el os para que acceda a los archivos locales
import requests
import json
import os

class LectorDelRepositorio:
   #Se crea una clase para que acceda a la Api de github
    
    
    def __init__(self, dueño, nombre_repo, branch = "main"):
        #se crea para el acceso al URL un dueño y a nombre del repo, esto para que en caso de querer cambiar de repo o se cambie de autor se pueda volver a acceder
        self.dueño = dueño
        self.nombre_repo = nombre_repo
        self.branch = branch
        #URL base de la API de contenidos de GitHub
        self.base_raw_url = f"https://raw.githubusercontent.com/{self.dueño}/{self.nombre_repo}/{self.branch}"
    



    def construir_url(self, nombre_archivo):
        #esta funcion ayudara a construir de manera mas sencilla la URL en proximas funciones
        return f"{self.base_raw_url}/{nombre_archivo}"




    def llamar_api_archivo(self, nombre_archivo):
        #aca se contruye el URL, con ayuda de la funcion anterior
        url = self.construir_url(nombre_archivo)
        headers = {'User-Agent': 'MiPrograma/1.0'} #el headers es la identificacion que se le envia al servidor para que GitHub nos acepte 
        #Aca llamamos directamente a la API
        try:
            response = requests.get(url, headers=headers, timeout=10)
            #Lanza un error si la peticion falló (ej. 404)
            response.raise_for_status()
            return response
            
        except requests.exceptions.HTTPError as e:
            #este "Except" lo que hace es que detecte el error HTTPS y lo encapsula en una variable "e", para que luego imprima cual fue el error
            print(f"Error HTTP al conectar con GitHub ({url}): {e}")
            return None
        except requests.exceptions.RequestException as e:
            #aca es parecido al anterior "except" con la diferencia que ahora el error es de conexion
            print(f"Error de conexión para {url}: {e}")
            return None




    def decodificar_y_parsear(self, response): 
      
        if response is None:
            #aca lo que va a hacer es que si se consigue un error en la funcion anterior, lo que va a retornar va a hacer "none", ya que no puede hacer nada si hubo un error
            return None
            
        try:
            #Apartir de aca empezamos a decodificar los datos 
            datos_utilizables = response.json()
            return datos_utilizables   
        except json.JSONDecodeError: #esto solo se activa si hay un error si el contenido no es un .json valido
            print(f"Error FATAL: El contenido del archivo en {response.url} no es un JSON válido.")
            return None
        




    def obtener_datos(self, ingredientes_archivo, menu_archivo):
        #Realizar las llamadas a la API
        response1 = self._llamar_api_archivo(ingredientes_archivo)
        response2 = self._llamar_api_archivo(menu_archivo)

        #Si alguna falló, no podemos continuar
        if not response1 or not response2:
            print("No se pudieron obtener uno o ambos archivos de la API.")
            return None, None
            
        #Decodificar y parsear las respuestas
      
        datos_utilizables_ingredientes = self._decodificar_y_parsear(response1)
        datos_utilizables_menu = self._decodificar_y_parsear(response2)
      

        #Si alguno falló en el parseo, retornamos None
        if not datos_utilizables_ingredientes or not datos_utilizables_menu:
            print("Fallo al decodificar o parsear uno o ambos archivos.")
            return None, None
            
        #Si llegamos aquí, todo fue exitoso
        print("Los archivos .json han sido cargados con exito")
        return datos_utilizables_ingredientes, datos_utilizables_menu
    



    def descargar_y_guardar_archivo(self, nombre_archivo_remoto, nombre_archivo_local):
        #Descarga y guarda los datos de repositorio a unos archivos locales.
        print(f"Descargando '{nombre_archivo_remoto}' a '{nombre_archivo_local}")

        response = self.llamar_api_archivo(nombre_archivo_remoto)
        datos = self.decodificar_y_parsear(response)

        if datos is None: #si detecta que la variable 'datos' esta vacia va a terminar la funcion
            print(f"No se pudieron descargar los datos para '{nombre_archivo_remoto}'")
            return False

        try: 
            with open(nombre_archivo_local, 'w', encoding='utf-8') as f: #abre o crea un archivo en la computadora, en el modo de escritura 'w'
                json.dump(datos, f, indent=4, ensure_ascii=False) #transforma un diccionario de python a un archivo .Json
                print(f"'{nombre_archivo_local}' guardado con exito.")
                return True
        except IOError as e:
            print(f"Error al guardar el archivo local '{nombre_archivo_local}': {e}")
            return False
    



    def cargar_archivo_local(self, nombre_archivo_local): #va a cargar cada uno de los archivos guardados en la maquina local
        if os.path.exists(nombre_archivo_local):
            try:
                with open(nombre_archivo_local, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error: El archivo local '{nombre_archivo_local}' no es un JSON valido")
                return None
            except IOError as e:
                print(f"Eror al leer el archivo local '{nombre_archivo_local}': {e}")
                return None
        else:
            print(f"Archivo local '{nombre_archivo_local}' no encontrado.")
            return None


