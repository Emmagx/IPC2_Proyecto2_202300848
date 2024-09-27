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
    movimientos_brazos = ListaSimpleEnlazada()  # Guarda la posición actual de cada brazo
    tiempos_ensamblaje = ListaSimpleEnlazada()  # Guarda si una línea está ensamblando (0 = no, 1 = ensamblando)
    instrucciones_por_linea = ListaSimpleEnlazada()  # Instrucciones para cada línea de ensamblaje
    
    # Inicializamos las posiciones de los brazos y tiempos de ensamblaje para cada línea de ensamblaje
    for _ in range(maquina.cantidad_lineas):
        movimientos_brazos.insertar(0)  # Todos los brazos empiezan en la posición 0
        tiempos_ensamblaje.insertar(0)  # Ninguna línea está ensamblando al principio
        instrucciones_por_linea.insertar(None)  # Inicialmente no hay instrucciones asignadas

    instrucciones = producto.elaboracion  # Las instrucciones del producto
    actual_instruccion = instrucciones.cabeza  # Primera instrucción

    # Almacenar las instrucciones por línea de ensamblaje
    while actual_instruccion:
        linea, componente = extraer_linea_componente(actual_instruccion.valor)
        instrucciones_por_linea.actualizar_por_posicion(linea - 1, (linea - 1, componente))  # Guardar instrucción en la lista
        actual_instruccion = actual_instruccion.siguiente

    ensamblando = False
    ensamblando_linea = -1
    
    # Mientras haya instrucciones por ejecutar en alguna línea
    while any(instrucciones_por_linea.obtener_por_posicion(i) is not None for i in range(maquina.cantidad_lineas)):
        tiempo_total += 1
        print(f"\n{tiempo_total}er segundo:")

        # Revisamos todas las líneas para mover brazos si es necesario
        for linea in range(maquina.cantidad_lineas):
            instruccion = instrucciones_por_linea.obtener_por_posicion(linea)
            if instruccion is not None:
                posicion_brazo = movimientos_brazos.obtener_por_posicion(linea)
                _, componente = instruccion

                # Si la línea no está ensamblando, mover el brazo
                if not ensamblando:
                    if posicion_brazo < componente:
                        # Mover el brazo hacia adelante, un paso por segundo
                        movimientos_brazos.actualizar_por_posicion(linea, posicion_brazo + 1)
                        print(f"Línea {linea + 1} moviendo brazo hacia el componente {componente}. Ahora en posición {posicion_brazo + 1}")
                    elif posicion_brazo > componente:
                        # Mover el brazo hacia atrás, un paso por segundo
                        movimientos_brazos.actualizar_por_posicion(linea, posicion_brazo - 1)
                        print(f"Línea {linea + 1} moviendo brazo hacia el componente {componente}. Ahora en posición {posicion_brazo - 1}")
                    elif posicion_brazo == componente:
                        # Si el brazo está en la posición correcta, ensamblar
                        ensamblando = True
                        ensamblando_linea = linea
                        tiempos_ensamblaje.actualizar_por_posicion(linea, 1)
                        instrucciones_por_linea.actualizar_por_posicion(linea, None)  # Marcar la instrucción como realizada
                        print(f"Línea {linea + 1} ensamblando componente {componente}")

        # Terminar ensamblaje
        if ensamblando:
            print(f"Línea {ensamblando_linea + 1} termina ensamblaje")
            ensamblando = False
            tiempos_ensamblaje.actualizar_por_posicion(ensamblando_linea, 0)

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
