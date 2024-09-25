import xml.etree.ElementTree as ET
from backend.maquina import Maquina
from backend.producto import Producto
from utils.cadenaEnlazada import CadenaEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada as lista

import xml.etree.ElementTree as ET
from backend.maquina import Maquina
from backend.producto import Producto
from utils.cadenaEnlazada import CadenaEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada as lista

def leer_archivo_xml(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    maquinas = lista()
    instrucciones = lista()  # Inicializamos la lista de instrucciones
    print("Empezando lectura")

    for maquina in root.findall('Maquina'):
        nombre = maquina.find('NombreMaquina').text
        cantidad_lineas = int(maquina.find('CantidadLineasProduccion').text)
        cantidad_componentes = int(maquina.find('CantidadComponentes').text)
        print(f"Cantidad de líneas: {cantidad_lineas}, Cantidad de componentes: {cantidad_componentes}")
        tiempo_ensamblaje = int(maquina.find("TiempoEnsamblaje").text)
        nueva_maquina = Maquina(nombre, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje)

        for producto in maquina.find('ListadoProductos'):
            nombre_producto = producto.find('nombre').text
            elaboracion = producto.find('elaboracion').text
            nuevo_producto = Producto(nombre_producto, elaboracion)
            nueva_maquina.productos.insertar(nuevo_producto)
            print(f"Producto: {nombre_producto}, Elaboración: {elaboracion}, Máquina: {nombre}")

        maquinas.insertar(nueva_maquina)


    return maquinas