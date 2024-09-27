class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None
    
    def insertar(self, valor):
        nuevo_nodo = NodoArbol(valor)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo)
    
    def _insertar_recursivo(self, actual, nuevo_nodo):
        if nuevo_nodo.valor < actual.valor:
            if actual.izquierdo is None:
                actual.izquierdo = nuevo_nodo
            else:
                self._insertar_recursivo(actual.izquierdo, nuevo_nodo)
        else:
            if actual.derecho is None:
                actual.derecho = nuevo_nodo
            else:
                self._insertar_recursivo(actual.derecho, nuevo_nodo)
    
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, actual, valor):
        if actual is None or actual.valor == valor:
            return actual
        if valor < actual.valor:
            return self._buscar_recursivo(actual.izquierdo, valor)
        return self._buscar_recursivo(actual.derecho, valor)
    
    def recorrer_inorden(self):
        self._recorrer_inorden(self.raiz)
    
    def _recorrer_inorden(self, nodo):
        if nodo is not None:
            self._recorrer_inorden(nodo.izquierdo)
            print(nodo.valor, end=" ")
            self._recorrer_inorden(nodo.derecho)
