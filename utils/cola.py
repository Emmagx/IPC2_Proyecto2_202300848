class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
    
    def enqueue(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.is_empty():
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
    
    def dequeue(self):
        if not self.is_empty():
            valor = self.frente.valor
            self.frente = self.frente.siguiente
            if self.frente is None: 
                self.final = None
            return valor
        return None  # Cola vacía
    
    def peek(self):
        if not self.is_empty():
            return self.frente.valor
        return None
    
    def is_empty(self):
        return self.frente is None
