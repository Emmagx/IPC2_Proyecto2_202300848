from flask import Flask, render_template, request
import os
from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.analizador import analizarArchivo
from utils.procesarInstruccion import simular_proceso_creacion
from utils.salida import generar_salida_xml
from backend.fila import FilaTabla

app = Flask(__name__, template_folder="../templates", static_folder="../static")
componentes_lista = ListaSimpleEnlazada()
maquinas_lista = ListaSimpleEnlazada()
productos = ListaSimpleEnlazada()
@app.route('/',  methods=['POST', 'GET'])
def upload_file():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return "No se ha seleccionado ningún archivo."
        
        file = request.files['file']
        if file.filename == '':
            return "Nombre de archivo vacío."
        
        if file:
            upload_path = os.path.join("uploads", file.filename)
            file.save(upload_path)

            maquinas = analizarArchivo(upload_path)

            componentes_lista.vaciar()
            maquinas_lista.vaciar()
            productos.vaciar()

            tabla_datos = ListaSimpleEnlazada()
            actual_maquina = maquinas.cabeza
            while actual_maquina:
                maquina = actual_maquina.valor
                
                for i in range(maquina.componentes.longitud()):
                    componente = f"Componente {i + 1}"
                    componentes_lista.insertar(componente)

                actual_producto = maquina.productos.cabeza
                while actual_producto:
                    producto = actual_producto.valor
                    fila = FilaTabla(maquina.nombre, producto.nombre)

                    if not maquinas_lista.contiene(maquina.nombre):
                        maquinas_lista.insertar(maquina.nombre)

                    if not productos.contiene(producto.nombre):
                        productos.insertar(producto.nombre)

                    tabla_datos.insertar(fila)
                    actual_producto = actual_producto.siguiente
                actual_maquina = actual_maquina.siguiente
            
            return render_template('index.html', datos=tabla_datos, componentes=componentes_lista, maquinas=maquinas_lista, producto=productos)
    return render_template('index.html')       


@app.route('/simulate', methods=['POST'])
def simulate():
    maquina_nombre = request.form['maquina']
    producto_nombre = request.form['producto']

    actual_maquina = maquinas_lista.cabeza
    maquina = None
    producto = None
    while actual_maquina:
        if actual_maquina.valor.maquina == maquina_nombre:
            maquina = actual_maquina.valor.maquina
            break
        actual_maquina = actual_maquina.siguiente

    actual_producto = producto.cabeza
    while actual_producto:
        if actual_producto.valor.producto == producto_nombre:
            producto = actual_producto.valor.producto
            break
        actual_producto = actual_producto.siguiente

    if maquina and producto:
        simular_proceso_creacion(maquina, producto)
        return f"Simulación del producto {producto} en la máquina {maquina} completada."
    else:
        return "Error en la simulación: Máquina o Producto no encontrados."

if __name__ == '__main__':
    app.run(debug=True)
