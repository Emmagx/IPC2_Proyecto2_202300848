class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None        

class ListaSimpleEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def insertar(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def eliminar(self, valor):
        actual = self.cabeza
        anterior = None
        while actual and actual.valor != valor:
            anterior = actual
            actual = actual.siguiente
        if actual is None:
            return False
        if anterior is None:
            self.cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente
        return True
    
    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.valor, end=" -> ")
            actual = actual.siguiente
        print("None")
