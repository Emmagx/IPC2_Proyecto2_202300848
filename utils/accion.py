from utils.listaSimplementeEnlazada import ListaSimpleEnlazada

class AccionEnsamblaje:
    def __init__(self, linea, accion, do):
        self.linea = linea
        self.componente = accion
        self.do = do

def agregar_accion(self, segundo, linea, accion, do):
    while len(self.segundos) < segundo:
        self.segundos.insertar(ListaSimpleEnlazada())

    acciones_en_segundo = self.segundos.obtener_por_posicion(segundo - 1)

    accion_ensamblaje = AccionEnsamblaje(linea, accion, do)
    print(f"Adding action: Line {linea}, Action {accion} at second {segundo}")
    
    acciones_en_segundo.insertar(accion_ensamblaje)