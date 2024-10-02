from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.listaDoblementeEnlazada import ListaDobleEnlazada
from utils.analizador import analizarArchivo
from utils.Historial import HistorialEnsamblaje
from utils.salida import generar_salida_xml
from utils.generarHTML import generar_reporte_html
from utils.generarGrafo import generar_grafo_ensamblaje

def extraer_linea_componente(instruccion):
    linea_caracter = instruccion.obtener(1)  
    componente_caracter = instruccion.obtener(3)
    return int(linea_caracter), int(componente_caracter)

def simular_proceso_creacion(maquina, producto):
    print(f"Simulando ensamblaje para el producto: {producto.nombre}")
    tiempo_total = 0
    movimientos_brazos = ListaSimpleEnlazada()
    instrucciones_por_linea = ListaSimpleEnlazada()
    producto.historial_ensamblaje = HistorialEnsamblaje()

    for _ in range(maquina.cantidad_lineas):
        movimientos_brazos.insertar(0)
        instrucciones_por_linea.insertar(None)

    instrucciones = producto.elaboracion
    actual_instruccion = instrucciones.cabeza
    while actual_instruccion:
        linea, componente = extraer_linea_componente(actual_instruccion.valor)
        instrucciones_por_linea.actualizar_por_posicion(linea - 1, (linea - 1, componente))
        actual_instruccion = actual_instruccion.siguiente

    ensamblando = False
    ensamblando_linea = -1

    # Mientras haya instrucciones por ejecutar en alguna línea
    while any(instrucciones_por_linea.obtener_por_posicion(i) is not None for i in range(maquina.cantidad_lineas)):
        tiempo_total += 1
        print(f"\n{tiempo_total}er segundo:")

        for linea in range(maquina.cantidad_lineas):
            instruccion = instrucciones_por_linea.obtener_por_posicion(linea)
            if instruccion is not None:
                posicion_brazo = movimientos_brazos.obtener_por_posicion(linea)
                _, componente = instruccion

                if not ensamblando:
                    if posicion_brazo < componente:
                        movimientos_brazos.actualizar_por_posicion(linea, posicion_brazo + 1)
                        producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, componente)
                        print(f"Línea {linea + 1} moviendo brazo hacia el componente {componente}. Ahora en posición {posicion_brazo + 1}")
                    elif posicion_brazo > componente:
                        movimientos_brazos.actualizar_por_posicion(linea, posicion_brazo - 1)
                        producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, componente)
                        print(f"Línea {linea + 1} moviendo brazo hacia el componente {componente}. Ahora en posición {posicion_brazo - 1}")
                    elif posicion_brazo == componente:
                        ensamblando = True
                        ensamblando_linea = linea

                        producto.historial_ensamblaje.agregar_accion(tiempo_total, linea + 1, componente)
                        for t in range(1, maquina.tiempo_ensamblaje):
                            
                            print(f"Línea {linea + 1} ensamblando componente {componente}")
                            tiempo_total +=1
                        instrucciones_por_linea.actualizar_por_posicion(linea, None)

        if ensamblando:
            
            print(f"Línea {ensamblando_linea + 1} termina ensamblaje")
            
            ensamblando = False

    producto.tiempo_total_ensamblaje = tiempo_total
    print(f"Producto {producto.nombre} ensamblado en {tiempo_total} segundos.\n")

    ruta_reporte_html = f"static/reporte_{producto.nombre}.html"
    ruta_grafo = f"static/grafo_{producto.nombre}"
    
    
    
    # Generar el reporte HTML
    tiempo = generar_reporte_html(maquina, producto, ruta_reporte_html)
    
    # Generar el gráfico de ensamblaje
    generar_grafo_ensamblaje(producto, ruta_grafo)

    print(f"Reporte HTML generado: {ruta_reporte_html}")
    print(f"Grafo de ensamblaje generado: {ruta_grafo}")
    ruta_grafo = f"{ruta_grafo}.png"
    return ruta_grafo, ruta_reporte_html, tiempo
    
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