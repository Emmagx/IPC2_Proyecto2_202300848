from utils.analizador import analizarArchivo
from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.lecturaXML import leer_archivo_xml
from utils.cadenaEnlazada import CadenaEnlazada
from utils.procesarInstruccion import simular_proceso_creacion
def main():
    ruta_archivo_xml = 'entrada.xml'
    maquinas = ListaSimpleEnlazada()

    maquinas = analizarArchivo(ruta_archivo_xml)
    
    actual_maquina = maquinas.cabeza
    while actual_maquina:
        maquina = actual_maquina.valor
        print(f"Máquina: {maquina.nombre}")
        
        actual_producto = maquina.productos.cabeza
        while actual_producto: 
            producto = actual_producto.valor
            print(f"Producto: {producto.nombre}")
            
            print("Elaboración: ", end="")
            actual_palabra = producto.elaboracion.cabeza 
            while actual_palabra:
                print(actual_palabra.palabra, end=" ") 
                actual_palabra = actual_palabra.siguiente  
            print()
            
            simular_proceso_creacion(maquina)
            
            actual_producto = actual_producto.siguiente
        
        actual_maquina = actual_maquina.siguiente

if __name__ == "__main__":
    main()
