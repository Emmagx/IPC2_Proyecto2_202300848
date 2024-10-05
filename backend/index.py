from flask import Flask, render_template, request, send_file
import os
import glob
from utils.procesarInstruccion import ejecutar_simulacion
from utils.listaSimplementeEnlazada import ListaSimpleEnlazada
from utils.analizador import analizarArchivo
from utils.procesarInstruccion import simular_proceso_creacion
from utils.salida import generar_salida_xml
from backend.fila import FilaTabla
from backend.maquina import Maquina
from backend.producto import Producto
from flask import jsonify
from backend.reporte import Reporte

app = Flask(__name__, template_folder="../templates", static_folder="../static")

componentes_lista = ListaSimpleEnlazada()
maquinas_lista = ListaSimpleEnlazada()
productos = ListaSimpleEnlazada()
global maquinas
global tabla_datos
tabla_datos = ListaSimpleEnlazada()
maquinas = ListaSimpleEnlazada()
global upload_path
upload_path = ""

@app.route('/', methods=['POST', 'GET'])
def upload_file():

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No se ha seleccionado ningún archivo."
        
        file = request.files['file']
        if file.filename == '':
            return "Nombre de archivo vacío."
        
        if file:
            global upload_path 
            upload_path = os.path.join("uploads", file.filename)
            file.save(upload_path)

            global maquinas
            maquinas = analizarArchivo(upload_path)

            componentes_lista.vaciar()
            maquinas_lista.vaciar()
            productos.vaciar()
            global tabla_datos
            tabla_datos = ListaSimpleEnlazada()
            actual_maquina = maquinas.cabeza
            while actual_maquina:
                maquina = actual_maquina.valor
                
                if not maquinas_lista.contiene(maquina):
                    maquinas_lista.insertar(maquina)

                for i in range(maquina.componentes.longitud()):
                    componente = f"Componente {i + 1}"
                    componentes_lista.insertar(componente)

                actual_producto = maquina.productos.cabeza
                while actual_producto:
                    producto = actual_producto.valor
                    
                    if not productos.contiene(producto):
                        productos.insertar(producto)

                    fila = FilaTabla(maquina.nombre, producto.nombre)
                    tabla_datos.insertar(fila)

                    actual_producto = actual_producto.siguiente
                actual_maquina = actual_maquina.siguiente

            nombres_maquinas = maquinas_lista.obtener_nombres()
            nombres_productos = productos.obtener_nombres()
            
            return render_template('index.html', datos=tabla_datos, componentes=None, maquinas=nombres_maquinas, producto=nombres_productos, report_html=None)

    return render_template('index.html', report_html=None, )

@app.route('/simulate', methods=['POST'])
def simulate():
    maquina_nombre = request.form['maquina']
    producto_nombre = request.form['producto']

    actual_maquina = maquinas_lista.cabeza
    maquina = None
    producto_encontrado = None

    # Buscar la máquina y el producto seleccionados
    while actual_maquina:
        maquina_actual = actual_maquina.valor
        if isinstance(maquina_actual, Maquina) and maquina_actual.nombre == maquina_nombre:
            maquina = maquina_actual
            actual_producto = maquina.productos.cabeza
            while actual_producto:
                producto_actual = actual_producto.valor
                if isinstance(producto_actual, Producto) and producto_actual.nombre == producto_nombre:
                    producto_encontrado = producto_actual
                    break
                actual_producto = actual_producto.siguiente
            break
        actual_maquina = actual_maquina.siguiente

    # Si se encuentra la máquina y el producto
    if maquina and producto_encontrado:
        grafo_path, pasos, time = simular_proceso_creacion(maquina, producto_encontrado)

        nombres_maquinas = maquinas_lista.obtener_nombres()
        nombres_productos = productos.obtener_nombres()

        return render_template(
            'index.html',
            datos=tabla_datos,
            componentes=None,
            maquinas=nombres_maquinas,
            producto=nombres_productos,
            grafo_image=grafo_path,
            report_html=pasos,
            tiempo=time,
            error=None
        )
    else:
        # Si no se encuentra la máquina o el producto, devolvemos la misma página con un mensaje de error
        nombres_maquinas = maquinas_lista.obtener_nombres()
        nombres_productos = productos.obtener_nombres()

        return render_template(
            'index.html',
            datos=tabla_datos,
            componentes=None,
            maquinas=nombres_maquinas,
            producto=nombres_productos,
            grafo_image=None,
            report_html=None,
            tiempo=None,
            error="No se encontró la máquina o el producto seleccionados. Por favor, intente nuevamente."
        )

@app.route('/get_components/<maquina_nombre>', methods=['GET'])
def get_components(maquina_nombre):
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

    return componentes.to_json()

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/reportes', methods=['GET'])
def reportes():
    ruta_static = os.path.join(app.static_folder)
    archivos_html = glob.glob(os.path.join(ruta_static, "*.html"))

    reportes_info = ListaSimpleEnlazada()
    
    for archivo in archivos_html:
        nombre_archivo = os.path.basename(archivo)
        reporte = Reporte(nombre_archivo, archivo)
        reportes_info.insertar(reporte)

    return render_template('reportes.html', reportes=reportes_info.to_list_enlazada())

@app.route('/Salida', methods=['POST'])
def salida():
    # Aquí generamos la ruta de salida del archivo XML
    ruta_archivo_xml = upload_path
    ruta_salida_xml = os.path.join("salidas", "reporte_salida.xml")  # Especifica la ruta donde se guardará el archivo de salida

    # Ejecutar la simulación
    ejecutar_simulacion(ruta_archivo_xml, ruta_salida_xml)
    
    # Enviar el archivo generado al cliente
    return send_file(ruta_salida_xml, as_attachment=True)

@app.route('/delete_files', methods=['POST'])
def delete_files():
    ruta_static = os.path.join(app.static_folder)
    archivos_png = glob.glob(os.path.join(ruta_static, "*.png"))
    archivos_html = glob.glob(os.path.join(ruta_static, "*.html"))

    # Eliminar archivos
    for archivo in archivos_png + archivos_html:
        try:
            os.remove(archivo)
            print(f"Archivo eliminado: {archivo}")
        except Exception as e:
            print(f"No se pudo eliminar el archivo {archivo}: {e}")

    return jsonify({"message": "Archivos eliminados exitosamente."}), 200

if __name__ == '__main__':
    app.run(debug=True)
