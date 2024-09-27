class NodoDoble:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListaDobleEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def insertar(self, valor):
        nuevo_nodo = NodoDoble(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.anterior = actual
    
    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.valor, end=" <-> ")
            actual = actual.siguiente
        print("None")
        
    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.valor
            actual = actual.siguiente
            
    def obtener_por_posicion(self, posicion):

            actual = self.cabeza
            contador = 0
            while actual:
                if contador == posicion:
                    return actual.valor
                actual = actual.siguiente
                contador += 1
            return None