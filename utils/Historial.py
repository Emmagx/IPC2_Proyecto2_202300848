from utils.listaSimplementeEnlazada import ListaSimpleEnlazada

class HistorialEnsamblaje:
    def __init__(self):
        self.segundos = ListaSimpleEnlazada()

    def agregar_accion(self, segundo, linea, accion):
        while len(self.segundos) < segundo:
            self.segundos.insertar(ListaSimpleEnlazada())

        acciones_en_segundo = self.segundos.obtener_por_posicion(segundo - 1)

        acciones_en_segundo.insertar(accion)

    def obtener_acciones_por_segundo(self, segundo):
        return self.segundos.obtener_por_posicion(segundo - 1)
