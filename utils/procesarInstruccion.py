from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada
from utils.cadenaEnlazada import CadenaEnlazada

def extraer_linea_componente(instruccion):
    linea_caracter = instruccion.obtener(0)
    componente_caracter = instruccion.obtener(0)
    print("linea " + linea_caracter)
    print("componente " + componente_caracter)

    return linea_caracter, componente_caracter


def simular_proceso_creacion(maquina):
    tiempo_total = 0
    lineas_ensamblaje = ListaDobleEnlazada()
    
    for i in range(maquina.cantidad_lineas):
        lineas_ensamblaje.insertar(0) 

    productos = maquina.productos

    actual_producto = productos.cabeza
    while actual_producto:
        producto = actual_producto.valor
        print(f"Simulando ensamblaje para el producto: {producto.nombre}")
        instrucciones = producto.elaboracion

        actual_instruccion = instrucciones.cabeza
        while actual_instruccion:
            instruccion = actual_instruccion.palabra
            print(f"Instrucción recibida: '{instruccion}'")
            
            
            actual_instruccion = actual_instruccion.siguiente
        
        actual_producto = actual_producto.siguiente
    
    print(f"Producto ensamblado en {tiempo_total} segundos.")
