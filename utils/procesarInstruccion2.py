from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.analizador import analizarArchivo
from utils.Historial import HistorialEnsamblaje
from utils.salida import generar_salida_xml
from utils.generarHTML import generar_reporte_html
from utils.generarGrafo import generar_grafo_ensamblaje

def extraer_linea_componente(instruccion):
    linea_caracter = instruccion.obtener(1)  # Asumimos que las posiciones empiezan desde 1
    componente_caracter = instruccion.obtener(3)
    return int(linea_caracter), int(componente_caracter)

def simular_proceso_creacion(maquina, producto):
    producto.historial_ensamblaje = HistorialEnsamblaje()
    print(f"Simulando ensamblaje para el producto: {producto.nombre}")
    tiempo_total = 0
    movimientos_brazos = ListaSimpleEnlazada()  # Lista para las posiciones de los brazos
    tiempos_ensamblaje = ListaSimpleEnlazada()  # Lista para el tiempo restante de ensamblaje de cada línea
    cola_ensamblaje = ListaSimpleEnlazada()  # Cola para las líneas que están esperando para ensamblar

    # Inicializamos las posiciones y tiempos de ensamblaje de las líneas
    for _ in range(maquina.cantidad_lineas):
        movimientos_brazos.insertar(0)  # Todas las líneas empiezan en la posición 1
        tiempos_ensamblaje.insertar(0)  # Inicialmente, ninguna línea está ensamblando

    instrucciones = producto.elaboracion.cabeza  # Empezamos con la primera instrucción
    ensamblando = False  # Para rastrear si alguna línea está ensamblando
    linea_ensamblando = None  # Para saber cuál línea está ensamblando actualmente

    while instrucciones or ensamblando or cola_ensamblaje.cabeza:
        tiempo_total += 1
        ensamblando = False

        for linea in range(0,maquina.cantidad_lineas):
            posicion_brazo = movimientos_brazos.obtener_por_posicion(linea)
            tiempo_restante = tiempos_ensamblaje.obtener_por_posicion(linea)

            # Si esta línea está ensamblando, reducimos su tiempo de ensamblaje
            if tiempo_restante > 1:
                tiempos_ensamblaje.actualizar_por_posicion(linea, tiempo_restante - 1)
                ensamblando = True  # Hay una línea ensamblando
                linea_ensamblando = linea  # Guardamos qué línea está ensamblando

                # Cuando termina el ensamblaje
            if tiempo_restante == 1:
                # cola_ensamblaje.eliminar_en_posicion(0)
                producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, f"Ensamblaje completado en la línea {linea + 1}")
                print(f"{tiempo_total}er segundo: Ensamblaje completado en la línea {linea + 1}")

            elif instrucciones:
                linea_actual, componente = extraer_linea_componente(instrucciones.valor)
                if linea_actual - 1  == linea:  # Si la instrucción corresponde a esta línea
                    if posicion_brazo < componente or posicion_brazo > componente:
                        # Movemos el brazo hacia adelante o hacia atrás
                        direccion = 1 if posicion_brazo < componente else -1
                        nueva_posicion = posicion_brazo + direccion
                        movimientos_brazos.actualizar_por_posicion(linea, nueva_posicion)
                        producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, f"Moviendo brazo hacia el componente {componente}")
                        print(f"{tiempo_total}er segundo: Moviendo brazo de la línea {linea + 1} hacia el componente {componente}")

                    # Si la línea llega a la posición del componente y no hay otra ensamblando
                    if posicion_brazo == componente and not ensamblando:
                        tiempos_ensamblaje.actualizar_por_posicion(linea, maquina.tiempo_ensamblaje -1 )
                        ensamblando = True
                        linea_ensamblando = linea
                        producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, f"Comenzando ensamblaje del componente {componente}")
                        print(f"{tiempo_total}er segundo: Comenzando ensamblaje del componente {componente} en la línea {linea + 1}")
                        tiempos_ensamblaje.actualizar_por_posicion(linea, tiempo_restante - 1)
                        instrucciones = instrucciones.siguiente  # Pasamos a la siguiente instrucción

                    elif posicion_brazo == componente and ensamblando:
                        # Si ya hay una línea ensamblando, agregamos esta línea a la cola
                        cola_ensamblaje.insertar(linea)
                        producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, f"Esperando ensamblaje en la línea {linea + 1}")
                        print(f"{tiempo_total}er segundo: Línea {linea + 1} esperando para ensamblar el componente {componente}")

        if not ensamblando and cola_ensamblaje.cabeza:
            linea_en_cola = cola_ensamblaje.obtener_por_posicion(0)  # Obtener la línea de la cola
            if linea_en_cola is not None:
                cola_ensamblaje.eliminar_en_posicion(0)
                tiempos_ensamblaje.actualizar_por_posicion(linea_en_cola, maquina.tiempo_ensamblaje)
                ensamblando = True
                linea_ensamblando = linea_en_cola
                producto.historial_ensamblaje.agregar_accion(tiempo_total, linea_en_cola + 1, f"Comenzando ensamblaje del componente en la línea {linea_en_cola + 1} (desde la cola)")
                print(f"{tiempo_total}er segundo: Comenzando ensamblaje del componente en la línea {linea_en_cola + 1} (desde la cola)")
            else:
                print(f"{tiempo_total}er segundo: No hay líneas en la cola.")




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