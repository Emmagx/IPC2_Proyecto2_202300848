class NodoTabla:
    def __init__(self, indice, bucket=None):
        self.indice = indice
        self.bucket = bucket
        self.siguiente = None

class TablaHash:
    def __init__(self, tamano=100):
        self.tamano = tamano
        self.primer_bucket = None  # Primer nodo que referencia los buckets
        self._crear_buckets(tamano)  # Método para crear los nodos de buckets

    def _crear_buckets(self, tamano):
        for i in range(tamano):
            self._agregar_bucket(i)

    def _agregar_bucket(self, indice):
        nuevo_nodo = NodoTabla(indice, Bucket())
        if self.primer_bucket is None:
            self.primer_bucket = nuevo_nodo
        else:
            actual = self.primer_bucket
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def _encontrar_bucket(self, indice):
        actual = self.primer_bucket
        while actual is not None:
            if actual.indice == indice:
                return actual.bucket
            actual = actual.siguiente
        raise IndexError(f'No se encontró el bucket con el índice {indice}')

    def _hash(self, clave):
        return hash(clave) % self.tamano

    def insertar(self, clave, valor):
        indice = self._hash(clave)
        bucket = self._encontrar_bucket(indice)
        bucket.insertar(clave, valor)

    def obtener(self, clave):
        indice = self._hash(clave)
        bucket = self._encontrar_bucket(indice)
        return bucket.obtener(clave)

    def eliminar(self, clave):
        indice = self._hash(clave)
        bucket = self._encontrar_bucket(indice)
        bucket.eliminar(clave)

    def contiene(self, clave):
        indice = self._hash(clave)
        bucket = self._encontrar_bucket(indice)
        return bucket.contiene(clave)

    def __str__(self):
        resultado = ""
        actual = self.primer_bucket
        while actual is not None:
            cadena_bucket = str(actual.bucket)
            if cadena_bucket != "Vacío":
                resultado += f"Índice {actual.indice}: {cadena_bucket}\n"
            actual = actual.siguiente
        return resultado.strip() if resultado else "Tabla Hash Vacía"
