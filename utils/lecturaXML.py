import xml.etree.ElementTree as ET
from backend.maquina import Maquina
from backend.producto import Producto
from utils.cadenaEnlazada import CadenaEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada as lista

def leer_archivo_xml(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    maquinas = lista()
    print("Empezando lectura")

    for maquina in root.findall('Maquina'):
        nombre = maquina.find('NombreMaquina').text
        cantidad_lineas = int(maquina.find('CantidadLineasProduccion').text)
        cantidad_componentes = int(maquina.find('CantidadComponentes').text)
        print(f"Cantidad de líneas: {cantidad_lineas}, Cantidad de componentes: {cantidad_componentes}")
        tiempo_ensamblaje = int(maquina.find("TiempoEnsamblaje").text)
        nueva_maquina = Maquina(nombre, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje)

        # Procesar los productos dentro de la máquina
        for producto in maquina.find('ListadoProductos'):
            nombre_producto = producto.find('nombre').text
            elaboracion_texto = producto.find('elaboracion').text
            
            nuevo_producto = Producto(nombre_producto)
            # Dividimos el texto de elaboración en palabras
            palabras = elaboracion_texto.split() 
            
            # Para cada palabra en las instrucciones
            for palabra in palabras:
                # Creamos una cadena enlazada con cada palabra (caracteres individuales)
                palabra_enlazada = CadenaEnlazada(palabra)  # Aquí la palabra se convierte en una CadenaEnlazada
                
                # Insertamos la palabra enlazada en la lista de elaboración del producto
                nuevo_producto.elaboracion.insertar(palabra_enlazada)

            # Insertamos el nuevo producto en la máquina
            nueva_maquina.productos.insertar(nuevo_producto)
            print(f"Producto: {nombre_producto}, Elaboración: {elaboracion_texto}, Máquina: {nombre}")

        # Insertamos la máquina en la lista de máquinas
        maquinas.insertar(nueva_maquina)

    return maquinas
