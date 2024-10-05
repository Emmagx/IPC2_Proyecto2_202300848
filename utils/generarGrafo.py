from graphviz import Digraph

def generar_grafo_ensamblaje(producto, ruta_salida_grafo):
    dot = Digraph(comment=f"Proceso de Ensamblado para {producto.nombre}")

    segundo_actual = 1

    actual_instruccion = producto.elaboracion.cabeza
    nodo_anterior = None

    while actual_instruccion:
        instruccion = actual_instruccion.valor

        instruccion_texto = str(instruccion)

        nodo =instruccion_texto

        dot.node(f"{segundo_actual}", nodo)

        if segundo_actual > 1 and nodo_anterior is not None:
           
            dot.edge(f"{segundo_actual - 1}", f"{segundo_actual}")  

        nodo_anterior = nodo

        actual_instruccion = actual_instruccion.siguiente
        segundo_actual += 1

    dot.render(ruta_salida_grafo, format='png', cleanup=True)
