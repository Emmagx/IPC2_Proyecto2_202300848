def generar_reporte_html(maquina, producto, ruta_salida_html):
    with open(ruta_salida_html, "w", encoding="utf-8") as archivo_html:
        archivo_html.write("<html><body>")
        archivo_html.write("<table border='1'><tr><th>Segundo</th><th>Línea</th><th>Componente</th></tr>")
        segundo = 1
        while segundo <= producto.historial_ensamblaje.segundos.longitud():
            acciones = producto.historial_ensamblaje.obtener_acciones_por_segundo(segundo)
            if acciones:
                accion_actual = acciones.cabeza
                while accion_actual:
                    linea = accion_actual.valor.linea  # Accedemos a la línea
                    componente = accion_actual.valor.componente  # Accedemos al componente
                    archivo_html.write(f"<tr><td>{segundo}</td><td>{linea}</td><td>{componente}</td></tr>")
                    accion_actual = accion_actual.siguiente
            segundo += 1

        archivo_html.write("</table>")
        archivo_html.write("</body></html>")

    print(f"Reporte HTML guardado en {ruta_salida_html}")
    return segundo
