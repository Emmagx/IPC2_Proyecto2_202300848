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
    
    def vaciar(self):
        self.cabeza = None
    
    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.valor, end=" -> ")
            actual = actual.siguiente
        print("None")
        
    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.valor
            actual = actual.siguiente

    def __len__(self):
        contador = 0
        actual = self.cabeza
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

    def longitud(self):
        return self.__len__()

    def obtener_por_posicion(self, posicion):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == posicion:
                return actual.valor
            actual = actual.siguiente
            contador += 1
        return None
    
    def actualizar_por_posicion(self, posicion, nuevo_valor):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == posicion:
                actual.valor = nuevo_valor 
                return True
            actual = actual.siguiente
            contador += 1
        return False
    
    def contiene(self, valor):
        actual = self.cabeza
        while actual:
            if actual.valor == valor:
                return True
            actual = actual.siguiente
        return False
    
    def obtener_nombres(self):
        nombres = ListaSimpleEnlazada()
        actual = self.cabeza
        while actual:
            if hasattr(actual.valor, 'nombre'):
                nombres.insertar(actual.valor.nombre) 
            actual = actual.siguiente
        return nombres
    
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
    
    def to_list_enlazada(self):
        nueva_lista = ListaSimpleEnlazada()
        actual = self.cabeza
        while actual:
            nueva_lista.insertar(actual.valor)  # Copiamos el valor a la nueva lista enlazada
            actual = actual.siguiente
        return nueva_lista
