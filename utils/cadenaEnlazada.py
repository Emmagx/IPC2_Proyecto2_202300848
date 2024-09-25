class NodoPalabra:
    def __init__(self, palabra):
        self.palabra = palabra  # Almacenar la palabra completa
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
        self.insertar(cadena)

    def insertar(self, palabra):
        nuevo_nodo = NodoPalabra(palabra)  # Aquí se guarda la palabra completa
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
                return actual.palabra  # Retorna la palabra completa en la posición 'indice'
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
            yield actual.palabra  # Cambiado para iterar por palabras
            actual = actual.siguiente

    def obtener_subcadena(self, inicio, longitud):
        nueva_cadena = CadenaEnlazada()
        actual = self.cabeza
        contador = 0
        while actual and contador < inicio + longitud:
            if contador >= inicio:
                nueva_cadena.insertar(actual.palabra)
            actual = actual.siguiente
            contador += 1
        return nueva_cadena

    def convertir_a_numero(self):
        resultado = 0
        factor = 1
        actual = self.cabeza
        while actual:
            resultado += (ord(actual.palabra) - ord('0')) * factor
            factor *= 10
            actual = actual.siguiente
        return resultado
