class NodoCaracter:
    def __init__(self, caracter):
        self.caracter = caracter
        self.siguiente = None

class CadenaEnlazada:
    def __init__(self, cadena=None):
        self.cabeza = None
        if cadena is not None:
            if isinstance(cadena, str):
                self.crear_enlazada(cadena)
            elif isinstance(cadena, CadenaEnlazada):
                self.cabeza = cadena.cabeza  # Copiar la cabeza de otra cadena enlazada

    def crear_enlazada(self, cadena):
        for caracter in cadena:
            self.insertar(caracter)

    def insertar(self, caracter):
        nuevo_nodo = NodoCaracter(caracter)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener(self, indice):
        actual = self.cabeza
        contador = 0
        while actual:
            if contador == indice:
                return actual.caracter
            actual = actual.siguiente
            contador += 1
        return None  # Si el índice está fuera de rango

    def longitud(self):
        contador = 0
        actual = self.cabeza
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.caracter  # Cambiado de valor a caracter
            actual = actual.siguiente
            
    def obtener_subcadena(self, inicio, longitud):

        nueva_cadena = CadenaEnlazada()
        actual = self.cabeza
        contador = 0
        while actual and contador < inicio + longitud:
            if contador >= inicio:
                nueva_cadena.insertar(actual.caracter)
            actual = actual.siguiente
            contador += 1
        return nueva_cadena

    def convertir_a_numero(self):
        resultado = 0
        factor = 1
        actual = self.cabeza
        while actual:
            resultado += (ord(actual.caracter) - ord('0')) * factor
            factor *= 10
            actual = actual.siguiente
        return resultado
