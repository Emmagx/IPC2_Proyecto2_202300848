import os
import glob
from utils.procesarInstruccion import ejecutar_simulacion


if __name__ == "__main__":
    ruta_archivo_xml = 'ArchivoPrueba.xml'
    ruta_salida = 'static/salida.xml'
    ejecutar_simulacion(ruta_archivo_xml, ruta_salida)
