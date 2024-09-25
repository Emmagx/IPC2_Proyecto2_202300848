from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.cadenaEnlazada import CadenaEnlazada

class Producto:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self.elaboracion = CadenaEnlazada(elaboracion)
        self.componentes = ListaSimpleEnlazada()