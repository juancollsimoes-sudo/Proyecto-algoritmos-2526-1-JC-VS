# Proyecto: Hot Dog CCS 🌭

Este proyecto es un sistema de gestión para un negocio de perros calientes, desarrollado como parte del curso de Algoritmos y Programación (BPTSP05) de la Universidad Metropolitana.

El objetivo es crear una aplicación de consola en Python que permita a un empresario gestionar los ingredientes, el inventario y el menú de su restaurante, así como simular las ventas de un día.

## 1. Flujo de Datos y Configuración

El sistema tiene un flujo de datos específico requerido por el proyecto:

1.  **Descarga Inicial de Datos**: Al comenzar, el programa debe conectarse a un repositorio de GitHub (`https://github.com/FernandoSapient/BPTSP05_2526-1`) para descargar los archivos JSON base (ingredientes y menú) usando la API de GitHub
2.  **Persistencia Local**: El programa **no** envía información nueva a la API. Cualquier cambio, nuevo ingrediente, o actualización de inventario se almacena en archivos JSON locales (en el directorio del programa).
3.  **Carga de Datos**: Al iniciar, el programa carga tanto los datos descargados de la API como los datos locales para tener el estado más actualizado.

## 2. Instalación y Ejecución

Sigue estos pasos para poner en marcha el sistema:

### Paso 1: Instalar Dependencias

Este proyecto requiere la biblioteca `requests` para descargar los archivos de datos iniciales desde GitHub.

```bash
pip install requests
````

## License
Programa hecho por Juan Coll y Valeria Solorzano