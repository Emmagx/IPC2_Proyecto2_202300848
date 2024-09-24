from utils.analizador import analizarArchivo
from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.lecturaXML import leer_archivo_xml


def main():
    ruta_archivo_xml = 'entrada.xml'  # Cambia esto por la ruta correcta a tu archivo XML

    # 1. Analizar el archivo XML
    maquinas, instrucciones = analizarArchivo(ruta_archivo_xml)

if __name__ == "__main__":
    main()
