from utils.lecturaXML import leer_archivo_xml
import xml.etree.ElementTree as ET
from utils.cadenaEnlazada import CadenaEnlazada
from utils.listaSimplementeEnlazada import ListaSimpleEnlazada  # Para almacenar las instrucciones

def analizarArchivo(ruta):
    maquinas = ListaSimpleEnlazada()
    maquinas, elaboracion = leer_archivo_xml(ruta)

    for index, maquina in enumerate(maquinas):
        for j in range(1, maquina.cantidad_componentes + 1):
            nombre_componente = f"componente{index + 1}_{j}"
            maquina.componentes.insertar(nombre_componente) 
            print(f"   Componente agregado a la Máquina {index + 1}: {nombre_componente}")

        actual = maquina.productos.cabeza
        while actual:
            print(f"   Producto: {actual.valor.nombre}, Elaboración: {actual.valor.elaboracion}")
            actual = actual.siguiente

    for index, maquina in enumerate(maquinas):
        print(f"Componentes de la Máquina {index + 1}:")
        maquina.componentes.mostrar()        
        
    return maquinas, elaboracion
