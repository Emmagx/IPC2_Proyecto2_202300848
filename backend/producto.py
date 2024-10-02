from utils.listaSimplementeEnlazada import ListaSimpleEnlazada as lista
from utils.Historial import HistorialEnsamblaje

class Producto:
    def __init__(self, nombre):
        self.nombre = nombre
        self.elaboracion = lista()
        self.instrucciones = HistorialEnsamblaje()
        self.componentes = lista()
    
    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.valor
            actual = actual.siguiente