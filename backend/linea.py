from utils.cola import Cola
class Linea:
    def __init__(self, numero, cantidad_componentes):
        self.numero = numero
        self.componente_actual = 0
        self.cantidad_componentes = cantidad_componentes
        self.movimientos = Cola()  # Para registrar las acciones

    def mover_brazo(self, componente):
        if componente > self.componente_actual:
            self.movimientos.enqueue(f"Mover brazo - Componente {componente}")
            self.componente_actual = componente
        elif componente == self.componente_actual:
            self.ensamblar()
        else:
            self.movimientos.enqueue(f"Mover brazo hacia atrás - Componente {componente}")
            self.componente_actual = componente

    def ensamblar(self):
        self.movimientos.enqueue(f"Ensamblar Componente {self.componente_actual}")
