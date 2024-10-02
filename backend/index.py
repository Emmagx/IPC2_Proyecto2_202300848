from flask import Flask, render_template, request
import os
from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.analizador import analizarArchivo
from utils.procesarInstruccion import simular_proceso_creacion
from utils.salida import generar_salida_xml
from backend.fila import FilaTabla
from backend.maquina import Maquina
from backend.producto import Producto
from flask import jsonify

app = Flask(__name__, template_folder="../templates", static_folder="../static")
componentes_lista = ListaSimpleEnlazada()
maquinas_lista = ListaSimpleEnlazada()
productos = ListaSimpleEnlazada()
global maquinas
global tabla_datos
tabla_datos = ListaSimpleEnlazada()
maquinas = ListaSimpleEnlazada()

@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No se ha seleccionado ningún archivo."
        
        file = request.files['file']
        if file.filename == '':
            return "Nombre de archivo vacío."
        
        if file:
            upload_path = os.path.join("uploads", file.filename)
            file.save(upload_path)

            global maquinas
            maquinas = analizarArchivo(upload_path)

            # Limpiar listas
            componentes_lista.vaciar()
            maquinas_lista.vaciar()
            productos.vaciar()
            global tabla_datos
            tabla_datos = ListaSimpleEnlazada()
            actual_maquina = maquinas.cabeza
            while actual_maquina:
                maquina = actual_maquina.valor
                
                # Guardar la máquina completa en la lista de máquinas
                if not maquinas_lista.contiene(maquina):
                    maquinas_lista.insertar(maquina)

                # Procesar los componentes
                for i in range(maquina.componentes.longitud()):
                    componente = f"Componente {i + 1}"
                    componentes_lista.insertar(componente)

                # Procesar productos
                actual_producto = maquina.productos.cabeza
                while actual_producto:
                    producto = actual_producto.valor
                    
                    # Guardar el producto completo en la lista de productos
                    if not productos.contiene(producto):
                        productos.insertar(producto)

                    # Insertar fila en la tabla
                    fila = FilaTabla(maquina.nombre, producto.nombre)
                    tabla_datos.insertar(fila)

                    actual_producto = actual_producto.siguiente
                actual_maquina = actual_maquina.siguiente

            # Extraer los nombres de las máquinas y productos para los comboboxes
            nombres_maquinas = maquinas_lista.obtener_nombres()  # Usar el nuevo método
            nombres_productos = productos.obtener_nombres()  # Usar el nuevo método
            
            return render_template('index.html', datos=tabla_datos, componentes=None, maquinas=nombres_maquinas, producto=nombres_productos, report_html = None)

    return render_template('index.html', report_html = None)

@app.route('/simulate', methods=['POST'])
def simulate():
    maquina_nombre = request.form['maquina']
    producto_nombre = request.form['producto']

    actual_maquina = maquinas_lista.cabeza
    maquina = None
    producto_encontrado = None

    # Buscar la máquina seleccionada por nombre en la lista de objetos Maquina
    while actual_maquina:
        maquina_actual = actual_maquina.valor
        if isinstance(maquina_actual, Maquina):
            if maquina_actual.nombre == maquina_nombre:  # Comparar por nombre
                maquina = maquina_actual
                
                # Buscar el producto dentro de la máquina seleccionada
                actual_producto = maquina.productos.cabeza
                while actual_producto:
                    producto_actual = actual_producto.valor
                    if isinstance(producto_actual, Producto):
                        if producto_actual.nombre == producto_nombre:  # Comparar por nombre
                            producto_encontrado = producto_actual
                            break
                    actual_producto = actual_producto.siguiente
                break
        actual_maquina = actual_maquina.siguiente

    # Verificar que se encontró la máquina y el producto
    if maquina and producto_encontrado:
        # Simular el proceso de creación
        grafo_path, pasos, time = simular_proceso_creacion(maquina, producto_encontrado)

        # Guardar el HTML de pasos
        report_html_path = f"/static/reporte_{producto_encontrado.nombre}.html"
        # with open(report_html_path, 'w') as file:
        #     file.write(pasos)

        # Preparar datos para renderizar
        nombres_maquinas = maquinas_lista.obtener_nombres()
        nombres_productos = productos.obtener_nombres()

        return render_template(
            'index.html',
            datos=tabla_datos,
            componentes=componentes_lista,
            maquinas=nombres_maquinas,
            producto=nombres_productos,
            grafo_image=grafo_path,
            report_html=pasos,
            tiempo=time
        )
    else:
        return "Error en la simulación: Máquina o Producto no encontrados."

@app.route('/get_components/<maquina_nombre>', methods=['GET'])
def get_components(maquina_nombre):
    # Buscar la máquina en la lista
    actual_maquina = maquinas_lista.cabeza
    componentes = ListaSimpleEnlazada()

    while actual_maquina:
        maquina = actual_maquina.valor
        if isinstance(maquina, Maquina) and maquina.nombre == maquina_nombre:
            actual_componente = maquina.componentes.cabeza
            while actual_componente:
                componentes.insertar(actual_componente.valor)
                actual_componente = actual_componente.siguiente
            break
        actual_maquina = actual_maquina.siguiente

    # Devuelve el JSON manualmente generado
    return componentes.to_json()



if __name__ == '__main__':
    app.run(debug=True)
