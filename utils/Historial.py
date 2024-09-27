from utils.listaSimplementeEnlazada import ListaSimpleEnlazada

class HistorialEnsamblaje:
    def __init__(self):
        self.segundos = ListaSimpleEnlazada() 
    
    def agregar_accion(self, segundo, linea, accion):
        
        acciones_en_segundo = self.segundos.obtener_por_posicion(segundo - 1)
        if not acciones_en_segundo:
            acciones_en_segundo = ListaSimpleEnlazada()
            self.segundos.insertar(acciones_en_segundo)
        acciones_en_segundo.insertar(f"Línea {linea}: {accion}")
    
    def obtener_acciones_por_segundo(self, segundo):
        return self.segundos.obtener_por_posicion(segundo - 1)
