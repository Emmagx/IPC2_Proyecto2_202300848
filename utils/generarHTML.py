def generar_reporte_html(maquina, producto, ruta_salida_html):
    with open(ruta_salida_html, "w", encoding="utf-8") as archivo_html:
        archivo_html.write("<html><head><title>Reporte Simulación</title></head><body>")
        archivo_html.write(f"<h1>Reporte de Simulación para {producto.nombre}</h1>")
        archivo_html.write(f"<p>Máquina: {maquina.nombre}</p>")
        archivo_html.write(f"<p>Tiempo total de ensamblaje: {producto.tiempo_total_ensamblaje} segundos</p>")
        
        archivo_html.write("<table border='1'><tr><th>Segundo</th><th>Línea</th><th>Acción</th></tr>")

        segundo = 1
        for acciones in producto.historial_ensamblaje.segundos:
            if acciones:
                for accion in acciones:
                    linea, accion_realizada = accion
                    archivo_html.write(f"<tr><td>{segundo}</td><td>{linea}</td><td>{accion_realizada}</td></tr>")
            segundo += 1
        
        archivo_html.write("</table>")
        archivo_html.write("</body></html>")
