from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada
from utils.cadenaEnlazada import CadenaEnlazada
from utils.analizador import analizarArchivo

def extraer_linea_componente(instruccion):
    linea_caracter = instruccion.obtener(1)  
    componente_caracter = instruccion.obtener(3)
    return int(linea_caracter), int(componente_caracter)

def simular_proceso_creacion(maquina, producto):
    print(f"Simulando ensamblaje para el producto: {producto.nombre}")
    tiempo_total = 0
    movimientos_brazos = ListaSimpleEnlazada()  
    tiempos_ensamblaje = ListaSimpleEnlazada()  
    
    # Inicializar los movimientos y ensamblajes
    for _ in range(maquina.cantidad_lineas):
        movimientos_brazos.insertar(0)
        tiempos_ensamblaje.insertar(0)

    instrucciones = producto.elaboracion
    actual_instruccion = instrucciones.cabeza
    while actual_instruccion:
        linea, componente = extraer_linea_componente(actual_instruccion.valor)
        linea -= 1  
        
        posicion_brazo = movimientos_brazos.obtener_por_posicion(linea)
        tiempo_movimiento = abs(posicion_brazo - componente) 
        
        tiempo_ensamblar = maquina.tiempo_ensamblaje - 1
        if tiempo_movimiento > 0:
            for t in range(1, tiempo_movimiento + 1):
                tiempo_total += 1
                print(f"{tiempo_total}er segundo: Moviendo brazo de la línea {linea + 1} hacia el componente {componente}")
        else:
            tiempo_total += 1

        for t in range(tiempo_ensamblar):
            tiempo_total += 1
            print(f"{tiempo_total}er segundo: Ensamblando componente {componente} en la línea {linea + 1}")
        
        movimientos_brazos.actualizar_por_posicion(linea, componente)

        actual_instruccion = actual_instruccion.siguiente

    print(f"Producto {producto.nombre} ensamblado en {tiempo_total} segundos.\n")

def ejecutar_simulacion(ruta_archivo_xml):
    maquinas = analizarArchivo(ruta_archivo_xml)
    actual_maquina = maquinas.cabeza

    while actual_maquina:
        maquina = actual_maquina.valor
        print(f"Simulando para la máquina: {maquina.nombre}")

        actual_producto = maquina.productos.cabeza
        while actual_producto:
            producto = actual_producto.valor
            print(f"Producto: {producto.nombre}")
            simular_proceso_creacion(maquina, producto)

            actual_producto = actual_producto.siguiente
        
        actual_maquina = actual_maquina.siguiente
