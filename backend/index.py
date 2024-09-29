from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Ruta principal que cargará la interfaz
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initialize', methods=['POST'])
def initialize_data():
    return "Datos inicializados correctamente."

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se ha seleccionado ningún archivo."
    
    file = request.files['file']
    if file.filename == '':
        return "Nombre de archivo vacío."
    
    if file:
        file.save(os.path.join("uploads", file.filename))
        return "Archivo cargado correctamente."

@app.route('/simulate', methods=['POST'])
def simulate():
    maquina = request.form['maquina']
    producto = request.form['producto']
    return f"Simulación del producto {producto} en la máquina {maquina}"

@app.route('/generate-report', methods=['POST'])
def generate_report():
    report_path = "reporte.html"
    return send_file(report_path, as_attachment=True)

@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    return "Gráfica generada correctamente."

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
