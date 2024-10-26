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
        
    def __len__(self):
        contador = 0
        actual = self.cabeza
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

    def longitud(self):
        return self.__len__()
    
    def contiene(self, valor):
        actual = self.cabeza
        while actual:
            if actual.valor == valor:
                return True
            actual = actual.siguiente
        return False
    
    def to_json(self):
        resultado = "["
        actual = self.cabeza
        while actual:
            resultado += f'"{actual.valor}"'
            actual = actual.siguiente
            if actual:
                resultado += ", "
        resultado += "]"
        return resultado