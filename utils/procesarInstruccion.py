from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada
from utils.analizador import analizarArchivo
from utils.Historial import HistorialEnsamblaje
from utils.salida import generar_salida_xml
from utils.generarHTML import generar_reporte_html
from utils.generarGrafo import generar_grafo_ensamblaje
from utils.instruccion import InstruccionesPendientes
from utils.instruccion import Instruccion
def extraer_linea_componente(instruccion):
    linea_caracter = instruccion.obtener(1)  
    componente_caracter = instruccion.obtener(3)
    return int(linea_caracter), int(componente_caracter)

def simular_proceso_creacion(maquina, producto):
    print(f"Simulando ensamblaje para el producto: {producto.nombre}")
    tiempo_total = 0
    movimientos_brazos = ListaSimpleEnlazada()  # Posición actual de los brazos en cada línea
    instrucciones_por_linea = ListaSimpleEnlazada()  # Instrucciones por cada línea
    tiempos_ensamblaje = ListaSimpleEnlazada()  # Tiempos restantes para ensamblar
    producto.historial_ensamblaje = HistorialEnsamblaje()

    # Inicializar las listas para cada línea
    for _ in range(maquina.cantidad_lineas):
        movimientos_brazos.insertar(0)
        instrucciones_por_linea.insertar(None)
        tiempos_ensamblaje.insertar(0)  # Tiempo de ensamblaje inicial en 0

    # Lista de todas las instrucciones del producto
    instrucciones = producto.elaboracion
    actual_instruccion = instrucciones.cabeza

    # Crear lista de instrucciones pendientes
    instrucciones_pendientes = InstruccionesPendientes(maquina.cantidad_lineas)

    # Procesar las instrucciones iniciales para cada línea
    while actual_instruccion:
        linea, componente = extraer_linea_componente(actual_instruccion.valor)
        instrucciones_pendientes.agregar_instruccion(linea - 1, componente)  # Agregar la instrucción a la lista de pendientes
        actual_instruccion = actual_instruccion.siguiente

    # Asignar la primera instrucción a cada línea
    for linea in range(maquina.cantidad_lineas):
        if instrucciones_pendientes.tiene_instrucciones_pendientes(linea):  # Si hay instrucciones pendientes en esa línea
            componente = instrucciones_pendientes.obtener_siguiente_instruccion(linea)
            instrucciones_por_linea.actualizar_por_posicion(linea, Instruccion(linea, componente))

    # Mientras haya instrucciones pendientes o en progreso
    contador = 0
    while any(instrucciones_por_linea.obtener_por_posicion(i) is not None or instrucciones_pendientes.tiene_instrucciones_pendientes(i) for i in range(maquina.cantidad_lineas)):
        if tiempo_total==0:
            tiempo_total =+ 1
        if contador > 0:
            tiempo_total += 1
            contador = 0
        print(f"\n{tiempo_total}er segundo:")

        # Recorrer cada línea y verificar si debe moverse o ensamblar
        for linea in range(maquina.cantidad_lineas):
            instruccion = instrucciones_por_linea.obtener_por_posicion(linea)
            tiempo_ensamblaje_restante = tiempos_ensamblaje.obtener_por_posicion(linea)
            
            # Si no hay más instrucciones en esta línea, saltar a la siguiente
            if instruccion is None and instrucciones_pendientes.tiene_instrucciones_pendientes(linea):
                componente = instrucciones_pendientes.obtener_siguiente_instruccion(linea)
                instrucciones_por_linea.actualizar_por_posicion(linea, Instruccion(linea, componente))
                instruccion = Instruccion(linea, componente)  # Crear nueva instrucción

            if instruccion is None:
                continue  # Si no hay instrucción, saltar a la siguiente línea

            posicion_brazo = movimientos_brazos.obtener_por_posicion(linea)
            componente = instruccion.componente
            componente -= 1 

            # Si la línea está ensamblando, continuar con el ensamblaje
            if tiempo_ensamblaje_restante > 0:
                print(f"Línea {linea + 1} ensamblando componente {componente + 1}")
                tiempos_ensamblaje.actualizar_por_posicion(linea, tiempo_ensamblaje_restante - 1)

                if tiempo_ensamblaje_restante -1 == 0:
                        print(f"Línea {linea + 1} termina de ensamblar el componente {componente}")
                        instrucciones_por_linea.actualizar_por_posicion(linea, None)
                        
                continue

            # Si el brazo no está en la posición correcta, mover el brazo
            if posicion_brazo < componente:
                print("posicion < componente")
                movimientos_brazos.actualizar_por_posicion(linea, posicion_brazo + 1)
                producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, f" {componente + 1}", "moviendo")
                print(f"Línea {linea + 1} moviendo brazo hacia el componente {componente}. Ahora en posición {posicion_brazo + 1}")
                contador += 1
            elif posicion_brazo > componente:
                print("posicion > componente")
                movimientos_brazos.actualizar_por_posicion(linea, posicion_brazo - 1)
                producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, f"{componente + 1}", "moviendo")
                print(f"Línea {linea + 1} moviendo brazo hacia el componente {componente}. Ahora en posición {posicion_brazo - 1}")
                contador += 1
            else:
                print("posicion == componente")
                tiempo_total += maquina.tiempo_ensamblaje
                producto.historial_ensamblaje.agregar_accion(tiempo_total , linea + 1, f"{componente + 1}", "ensamblaje")    
                tiempos_ensamblaje.actualizar_por_posicion(linea, maquina.tiempo_ensamblaje)
                contador = 0
                print(f"segundos {tiempo_total}")
                print(f"Línea {linea + 1} comenzando ensamblaje del componente {componente + 1}")
    
    producto.tiempo_total_ensamblaje = tiempo_total
    print(f"Producto {producto.nombre} ensamblado en {tiempo_total} segundos.\n")
    # Generar reporte y grafo como antes
    ruta_reporte_html = f"static/reporte_{producto.nombre}.html"
    ruta_grafo = f"static/grafo_{producto.nombre}"
    generar_reporte_html(maquina, producto, ruta_reporte_html)
    generar_grafo_ensamblaje(producto, ruta_grafo)
    print(f"Reporte HTML generado: {ruta_reporte_html}")
    print(f"Grafo de ensamblaje generado: {ruta_grafo}")

    return ruta_grafo + ".png", ruta_reporte_html, tiempo_total

    
def ejecutar_simulacion(ruta_archivo_xml, ruta_salida_xml):
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

    generar_salida_xml(maquinas, ruta_salida_xml)