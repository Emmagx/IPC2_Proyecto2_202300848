from utils.listaSimplementeEnlazada import ListaSimpleEnlazada as listita
class simulacion:
    def _init_(self, maquina, producto):  # Constructor de la simulación para UN PRODUCTO
        self.maquina = maquina
        self.producto = producto
        self.tiempo = 0
        self.elaborar = self.crearLista()
        self.posicionesBrazos = self.crearLineas()
        self.listaElab=self.crearLista2()
        self.coldDown = 0
        self.reporte=None
        self.matriz=None
        self.tiempoOptimo=0
        self.elaboOptima=False

    # Función para crear la lista de elaboración
    def crearLista(self):
        listaElaborar = listita()
        instrucciones = self.producto.elaboracion.split()
        for i in instrucciones:
            tupla = listita()  # Creo una lista para guardar la instrucción

            #Divido las intrucciones en L y C
            divi=i.split("C")

            l =int(divi[0][1:]) # Línea
            tupla.agregar(l)
            c = int(divi[1])  # Componente
            tupla.agregar(c)
            listaElaborar.agregar(tupla) # Agrego la instrucción a la lista
        return listaElaborar
    
    #Crea una copia de la lista pero sin la tupla (no es tupla de verdad aclaro xd)
    def crearLista2(self):
        listaelab=listita()
        instrucciones = self.producto.elaboracion.split()
        for i in instrucciones:
            listaelab.agregar(i)
        return listaelab

    # Función para crear la lista de brazos en las líneas
    def crearLineas(self):
        listaBrazos = listita()
        for i in range(self.maquina.lineas):
            brazo_linea = brazo(i + 1)  # Creamos un brazo para cada línea
            listaBrazos.agregar(brazo_linea)
        return listaBrazos

    # Función principal que simula el proceso
    def simular(self):
        cuenta = 0  # Contador de tiempo
        self.elaboOptima=True
        # Mientras haya elementos en la lista de elaboración
        ensamble = False
        nombreBloqueado = ""
        eliminar=False
        banderlistaelab=False

        
        Tiempos=listita() #Creo una Lista para guardar los datos de las listas
        while self.elaborar.tamaño > 0 or self.coldDown >= 0: # Mientras haya elementos en la lista de elaboración
            cuenta += 1 # Aumentamos el tiempo

            print(self.coldDown)

            print(f"Tiempo: {cuenta}")  # Imprimir el tiempo
            tiempo=listita() #Creo una lista para guardar los datos de las líneas
            tiempo.agregar(cuenta) #Agrego el tiempo a la lista

            #ciclo para desocupar los brazos y limpiar los mensajes
            for i in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                brazo=self.posicionesBrazos.encontrar(i) # Ubico el brazo

                if brazo.nombre != nombreBloqueado: # Si el brazo bloqueado es el que se está buscando
                    brazo.estado=False # Lo desocupo
                    brazo.mensaje="No hacer nada"
                else:
                    brazo.estado=False # Lo ocupo

            #Comprobando que se halla pasado ya la posición necesaria para eliminar el procedimiento
            if banderlistaelab:
                self.listaElab.eliminar(0)
                banderlistaelab=False    

            # Recorremos la lista de elaboración
            for i in range(self.elaborar.tamaño):
                instruccion = self.elaborar.encontrar(i)  # Ubico la tupla
                linea = instruccion.encontrar(0)  # Línea
                componente = instruccion.encontrar(1)  # Componente
                print(f"Línea: {linea} Componente: {componente}")

                # Recorremos la lista de brazos
                for j in range(self.posicionesBrazos.tamaño):
                    brazo = self.posicionesBrazos.encontrar(j)  # Ubico el brazo

                    if brazo.nombre == linea:
                        print(f"Brazo: {brazo.nombre} en la línea {brazo.posicionActual}")
                        if not brazo.estado and ( not brazo.bloqueo):  # Si el brazo está desocupado
                            brazo.estado = True  # Lo ocupo
                            
                            if brazo.posicionActual < componente:  # Si la posición actual es menor al componente
                                
                                if not brazo.bloqueo:  # Si no está bloqueado
                                    brazo.posicionActual += 1  # Avanzo el brazo
                                    brazo.mensaje= f"Mover brazo - componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(f"Brazo: {brazo.nombre} avanzando a la posición {brazo.posicionActual}")

                            elif brazo.posicionActual == componente:  # Si estamos en el componente
                                if not ensamble and (i==0):  # Si no se está ensamblando
                                    ensamble = True  # Se ensambla
                                    brazo.mensaje= f"Ensamblar componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(brazo.mensaje)

                                    brazo.bloqueo = True  # El brazo se desocupa
                                    nombreBloqueado = brazo.nombre # Guardo el nombre del brazo bloqueado

                                    posParaEliminar = i # Guardo la posición para eliminar
                                    eliminar=True # Elimino la tarea

                                    #self.elaborar.eliminar(i)  # Eliminamos la tarea completada
                                    self.coldDown = self.maquina.tiempo-1  # Iniciamos el tiempo de espera
                                else:
                                    print("Ensamble en proceso o a la espera de ensamble")
                            else:  # Si la posición actual es mayor al componente
                                if not brazo.bloqueo: # Si no está bloqueado
                                    brazo.posicionActual -= 1  # Retrocedemos el brazo
                                    brazo.mensaje= f"Mover brazo - componente {brazo.posicionActual}" #Guardo el mensaje
                                    print(brazo.mensaje)



            if eliminar: # Si se debe eliminar la tarea
                self.elaborar.eliminar(posParaEliminar) # Eliminamos la tarea completada
                eliminar=False # Ya no se debe eliminar
                print("Tarea eliminada")

            # Control de tiempo de espera (coldown)
            if self.coldDown > 0:
                print(f"Enfriamiento: {self.coldDown}")
                self.coldDown -= 1
            else:
                self.coldDown = -1
                for j in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                    brazo = self.posicionesBrazos.encontrar(j) # Ubico el brazo
                    if brazo.nombre == nombreBloqueado: # Si el brazo bloqueado es el que se está buscando
                        brazo.bloqueo = False # Se desbloquea
                        nombreBloqueado = "" 
                        banderlistaelab=True
                        print(f"Brazo {brazo.nombre} desbloqueado")
                        ensamble = False # Se desbloquea para que se pueda ensamblar

            #Ciclo para generar la lista de posiciones de los brazos
            for i in range(self.posicionesBrazos.tamaño): # Recorremos la lista de brazos
                brazo=self.posicionesBrazos.encontrar(i) # Ubico el brazo
                tiempo.agregar(brazo.mensaje) # Agrego el mensaje a la lista

            Tiempos.agregar(tiempo) # Agrego la lista de mensajes a la lista de tiempos

            print("------------------------------------------------------")
        self.matriz=Tiempos #Guardo la lista de tiempos en el reporte        
        

        #Probando que se guardó bien en la matriz :)
        for i in range(self.matriz.tamaño): # Recorremos la lista de tiempos
            for j in range(self.matriz.encontrar(i).tamaño):
                print(self.matriz.encontrar(i).encontrar(j), end=" | ") # Imprimimos el mensaje
            print() # Salto de línea
        #---------------------------------------------------------------------------------------
        self.tiempoOptimo=cuenta
        print(cuenta)