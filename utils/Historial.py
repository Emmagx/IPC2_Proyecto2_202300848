from utils.listaSimplementeEnlazada import ListaSimpleEnlazada

class HistorialEnsamblaje:
    def __init__(self):
        self.segundos = ListaSimpleEnlazada()

    def agregar_accion(self, segundo, linea, accion):
        while len(self.segundos) < segundo:
            self.segundos.insertar(ListaSimpleEnlazada())

        acciones_en_segundo = self.segundos.obtener_por_posicion(segundo - 1)
        
        if acciones_en_segundo is None:
            acciones_en_segundo = ListaSimpleEnlazada()
            self.segundos.actualizar_por_posicion(segundo - 1, acciones_en_segundo)

        acciones_en_segundo.insertar((linea, accion))

    def obtener_acciones_por_segundo(self, segundo):
        return self.segundos.obtener_por_posicion(segundo - 1)

    def obtener_por_posicion(self, posicion):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == posicion:
                return actual.valor
            actual = actual.siguiente
            contador += 1
        return None