class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaCircular:
    def __init__(self):
        self.cabeza = None
    
    def insertar_al_final(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
    
    def mostrar(self):
        if self.cabeza is None:
            return
        actual = self.cabeza
        while True:
            print(actual.valor, end=" -> ")
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        print()
