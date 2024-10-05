from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
class NodoPendiente:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class InstruccionesPendientes:
    def __init__(self, cantidad_lineas):
        self.lineas = ListaSimpleEnlazada()
        for _ in range(cantidad_lineas):
            self.lineas.insertar(ListaSimpleEnlazada())  # Cada línea tiene su propia lista de instrucciones pendientes

    def agregar_instruccion(self, linea, componente):
        lista_instrucciones = self.lineas.obtener_por_posicion(linea)
        lista_instrucciones.insertar(componente)

    def obtener_siguiente_instruccion(self, linea):
        lista_instrucciones = self.lineas.obtener_por_posicion(linea)
        if lista_instrucciones.cabeza is None:
            return None
        componente = lista_instrucciones.cabeza.valor
        lista_instrucciones.eliminar(componente)
        return componente

    def tiene_instrucciones_pendientes(self, linea):
        lista_instrucciones = self.lineas.obtener_por_posicion(linea)
        return lista_instrucciones.cabeza is not None

class Instruccion:
    def __init__(self, linea, componente):
        self.linea = linea
        self.componente = componente