import os
import glob
from utils.procesarInstruccion import ejecutar_simulacion

def eliminar_imagenes():
    # Busca todos los archivos .png, .dot y .html en el directorio actual y los elimina
    archivos_png = glob.glob("*.png")
    archivos_dot = glob.glob("*.dot")
    archivos_html = glob.glob("*.html")  # Agregar búsqueda para archivos HTML

    # Eliminar archivos .png
    for archivo in archivos_png:
        try:
            os.remove(archivo)
            print(f"Archivo eliminado: {archivo}")
        except Exception as e:
            print(f"No se pudo eliminar el archivo {archivo}: {e}")

    # Eliminar archivos .dot
    for archivo in archivos_dot:
        try:
            os.remove(archivo)
            print(f"Archivo eliminado: {archivo}")
        except Exception as e:
            print(f"No se pudo eliminar el archivo {archivo}: {e}")

    # Eliminar archivos .html
    for archivo in archivos_html:
        try:
            os.remove(archivo)
            print(f"Archivo eliminado: {archivo}")
        except Exception as e:
            print(f"No se pudo eliminar el archivo {archivo}: {e}")

if __name__ == "__main__":
    # Llamar a la función para eliminar imágenes antes de ejecutar la simulación
    eliminar_imagenes()
    
    ruta_archivo_xml = 'entrada.xml'
    ruta_salida = 'salida.xml'
    ejecutar_simulacion(ruta_archivo_xml, ruta_salida)
