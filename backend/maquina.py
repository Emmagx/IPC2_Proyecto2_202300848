from utils.listaDoblementeEnlazada import ListaDobleEnlazada
from utils.listaSimplementeEnlazada import ListaSimpleEnlazada

class Maquina:
    def __init__(self, nombre, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje):
        self.nombre = nombre
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.productos = ListaSimpleEnlazada()
        self.componentes = ListaDobleEnlazada()
