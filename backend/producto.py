from utils.listaSimplementeEnlazada import ListaSimpleEnlazada as lista
from utils.cadenaEnlazada import CadenaEnlazada

class Producto:
    def __init__(self, nombre):
        self.nombre = nombre
        self.elaboracion = lista()
        self.componentes = lista()