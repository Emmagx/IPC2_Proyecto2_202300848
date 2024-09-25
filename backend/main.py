from utils.analizador import analizarArchivo
from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.lecturaXML import leer_archivo_xml
from utils.cadenaEnlazada import CadenaEnlazada
from utils.procesarInstruccion import simular_proceso_creacion  # Asumimos que esta función está en simulador.py

def main():
    ruta_archivo_xml = 'entrada.xml'  # Cambia esto por la ruta correcta a tu archivo XML
    maquinas = ListaSimpleEnlazada()  # Instanciamos correctamente la lista de máquinas

    # 1. Analizar el archivo XML
    maquinas = analizarArchivo(ruta_archivo_xml)  # Analiza el archivo y devuelve las máquinas
    
    # 2. Iterar sobre las máquinas y sus productos
    actual_maquina = maquinas.cabeza
    while actual_maquina:  # Recorrer las máquinas
        maquina = actual_maquina.valor
        print(f"Máquina: {maquina.nombre}")
        
        # Iterar sobre los productos de la máquina
        actual_producto = maquina.productos.cabeza
        while actual_producto:  # Recorrer los productos
            producto = actual_producto.valor
            print(f"Producto: {producto.nombre}")
            
            # Imprimir la cadena de elaboración (iterando sobre las palabras)
            print("Elaboración: ", end="")
            actual_palabra = producto.elaboracion.cabeza  # Iteramos sobre la cadena de palabras
            while actual_palabra:
                print(actual_palabra.palabra, end=" ")  # Imprimir cada palabra con un espacio
                actual_palabra = actual_palabra.siguiente  # Avanzar al siguiente nodo (palabra)
            print()  # Salto de línea después de imprimir todas las palabras
            
            # Simular el proceso de ensamblaje para el producto
            simular_proceso_creacion(maquina)
            
            # Avanzar al siguiente producto
            actual_producto = actual_producto.siguiente
        
        # Avanzar a la siguiente máquina
        actual_maquina = actual_maquina.siguiente

if __name__ == "__main__":
    main()
