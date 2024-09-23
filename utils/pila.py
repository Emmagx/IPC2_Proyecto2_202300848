class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Pila:
    def __init__(self):
        self.cima = None
    
    def push(self, valor):
        nuevo_nodo = Nodo(valor)
        nuevo_nodo.siguiente = self.cima
        self.cima = nuevo_nodo
    
    def pop(self):
        if not self.is_empty():
            valor = self.cima.valor
            self.cima = self.cima.siguiente
            return valor
        return None  # Pila vacía
    
    def peek(self):
        if not self.is_empty():
            return self.cima.valor
        return None
    
    def is_empty(self):
        return self.cima is None
