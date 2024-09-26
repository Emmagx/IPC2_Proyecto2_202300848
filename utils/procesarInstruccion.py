from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada
from utils.cadenaEnlazada import CadenaEnlazada
from utils.analizador import analizarArchivo

# Método para extraer línea y componente
def extraer_linea_componente(instruccion):
    linea_caracter = instruccion.obtener(1)  # Línea está en la posición 1
    componente_caracter = instruccion.obtener(3)  # Componente está en la posición 3
    return int(linea_caracter), int(componente_caracter)

# Método para simular el proceso de creación de un producto
def simular_proceso_creacion(maquina, producto):
    print(f"Simulando ensamblaje para el producto: {producto.nombre}")
    tiempo_total = 0
    movimientos_brazos = ListaSimpleEnlazada()  # Guarda la posición actual de cada brazo
    tiempos_ensamblaje = ListaSimpleEnlazada()  # Guarda si una línea está ensamblando
    
    # Inicializamos las posiciones de los brazos y tiempos de ensamblaje para cada línea de ensamblaje
    for _ in range(maquina.cantidad_lineas):
        movimientos_brazos.insertar(0)  # Todos los brazos empiezan en la posición 0
        tiempos_ensamblaje.insertar(0)  # Inicialmente no están ensamblando

    instrucciones = producto.elaboracion  # Las instrucciones del producto
    actual_instruccion = instrucciones.cabeza  # Primera instrucción

    # Iterar sobre cada instrucción de ensamblaje
    while actual_instruccion:
        linea, componente = extraer_linea_componente(actual_instruccion.valor)
        linea -= 1  # Convertimos a índice de 0 (interno)
        
        # Obtener la posición actual del brazo y el tiempo de ensamblaje
        posicion_brazo = movimientos_brazos.obtener_por_posicion(linea)  
        
        # Calcular el tiempo necesario para mover el brazo al componente
        tiempo_movimiento = abs(posicion_brazo - componente)
        
        # Ensamblar una vez en lugar de múltiples veces
        tiempo_ensamblar = 1  # Solo ensamblamos una vez, no tantas veces como el componente

        # Solo mover el brazo si no está ya en la posición correcta
        if tiempo_movimiento > 0:
            for t in range(1, tiempo_movimiento + 1):
                tiempo_total += 1
                print(f"{tiempo_total}er segundo: Moviendo brazo de la línea {linea + 1} hacia el componente {componente}")
        else:
            tiempo_total += 1  # El brazo no se mueve pero cuenta el segundo

        # Ensamblar el componente
        print(f"{tiempo_total}er segundo: Ensamblando componente {componente} en la línea {linea + 1}")
        
        # Actualizar la posición del brazo (sin insertar, sino reemplazando)
        movimientos_brazos.actualizar_por_posicion(linea, componente)
        
        # Pasamos a la siguiente instrucción
        actual_instruccion = actual_instruccion.siguiente

    print(f"Producto {producto.nombre} ensamblado en {tiempo_total} segundos.\n")

# Método para ejecutar la simulación en base a un archivo XML
def ejecutar_simulacion(ruta_archivo_xml):
    maquinas = analizarArchivo(ruta_archivo_xml)  # Lee el archivo y obtiene la lista de máquinas
    actual_maquina = maquinas.cabeza  # Primera máquina

    while actual_maquina:
        maquina = actual_maquina.valor
        print(f"Simulando para la máquina: {maquina.nombre}")

        actual_producto = maquina.productos.cabeza  # Primer producto de la máquina
        while actual_producto:
            producto = actual_producto.valor
            print(f"Producto: {producto.nombre}")
            simular_proceso_creacion(maquina, producto)  # Simula el ensamblaje del producto

            actual_producto = actual_producto.siguiente  # Siguiente producto
        
        actual_maquina = actual_maquina.siguiente  # Siguiente máquina
