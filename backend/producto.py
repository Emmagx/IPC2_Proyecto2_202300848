from utils.listaSimplementeEnlazada import ListaSimpleEnlazada

class Producto:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self.elaboracion = elaboracion
        self.componentes = ListaSimpleEnlazada()