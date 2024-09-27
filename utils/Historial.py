from utils.listaSimplementeEnlazada import ListaSimpleEnlazada

class HistorialEnsamblaje:
    def __init__(self):
        self.segundos = ListaSimpleEnlazada()  # Lista que contendrá listas de acciones por cada segundo

    def agregar_accion(self, segundo, linea, accion):
        # Asegurarse de que la lista de segundos tenga suficiente espacio hasta el 'segundo' deseado
        while len(self.segundos) < segundo:
            self.segundos.insertar(ListaSimpleEnlazada())  # Insertar listas vacías hasta llegar al segundo correcto

        # Obtener la lista de acciones para el segundo especificado
        acciones_en_segundo = self.segundos.obtener_por_posicion(segundo - 1)
        # Insertar la acción en esa lista
        acciones_en_segundo.insertar(accion)

    def obtener_acciones_por_segundo(self, segundo):
        # Obtener las acciones del segundo dado (o None si no hay acciones en ese segundo)
        return self.segundos.obtener_por_posicion(segundo - 1)
