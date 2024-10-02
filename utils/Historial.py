from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.accion import AccionEnsamblaje
class HistorialEnsamblaje:
    def __init__(self):
        self.segundos = ListaSimpleEnlazada()

    def agregar_accion(self, segundo, linea, componente):
        # Asegúrate de que haya suficientes posiciones en 'segundos'
        while self.segundos.longitud() < segundo:
            self.segundos.insertar(ListaSimpleEnlazada())

        # Obtener la lista de acciones para el segundo correspondiente
        acciones_en_segundo = self.segundos.obtener_por_posicion(segundo - 1)

        # Si no hay acciones en este segundo, crear una nueva lista
        if acciones_en_segundo is None:
            acciones_en_segundo = ListaSimpleEnlazada()
            self.segundos.actualizar_por_posicion(segundo - 1, acciones_en_segundo)

        # Crear una nueva acción de ensamblaje y agregarla a la lista
        nueva_accion = AccionEnsamblaje(linea, componente)
        acciones_en_segundo.insertar(nueva_accion)

    def obtener_acciones_por_segundo(self, segundo):
        return self.segundos.obtener_por_posicion(segundo - 1)


    def obtener_por_posicion(self, posicion):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == posicion:
                return actual.valor
            actual = actual.siguiente
            contador += 1
        return None