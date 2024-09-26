from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada
from utils.cadenaEnlazada import CadenaEnlazada
from utils.analizador import analizarArchivo

def extraer_linea_componente(instruccion):
    linea_caracter = instruccion.obtener(0)
    componente_caracter = instruccion.obtener(0)
    print("linea " + linea_caracter)
    print("componente " + componente_caracter)

    return linea_caracter, componente_caracter

def simular_proceso_creacion(maquina, producto):
    print("Simulación en proceso de creación")
    tiempo_total = 0
    lineas_ensamblaje = ListaDobleEnlazada()
    
    for i in range(maquina.cantidad_lineas):
        lineas_ensamblaje.insertar(0)  

    print(f"Simulando ensamblaje para el producto: {producto.nombre}")
    instrucciones = producto.elaboracion

    actual_instruccion = instrucciones.cabeza
    while actual_instruccion:
        instruccion = actual_instruccion.valor
        print(f"Instrucción recibida: '{instruccion}'")
        actual_instruccion = actual_instruccion.siguiente
    
    print(f"Producto ensamblado en {tiempo_total} segundos.")

def ejecutar_simulacion(ruta_archivo_xml):
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
                print(actual_palabra.valor, end=" ")
                actual_palabra = actual_palabra.siguiente  
            print()
            simular_proceso_creacion(maquina, producto)
            
            actual_producto = actual_producto.siguiente
        
        actual_maquina = actual_maquina.siguiente
