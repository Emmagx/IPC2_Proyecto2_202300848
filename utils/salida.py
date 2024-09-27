import xml.etree.ElementTree as ET


def generar_salida_xml(maquinas, ruta_salida_xml):
    root = ET.Element("SalidaSimulacion")

    actual_maquina = maquinas.cabeza

    while actual_maquina:
        maquina = actual_maquina.valor
        maquina_elem = ET.SubElement(root, "Maquina")
        nombre_maquina = ET.SubElement(maquina_elem, "Nombre")
        nombre_maquina.text = maquina.nombre
        
        listado_productos = ET.SubElement(maquina_elem, "ListadoProductos")

        actual_producto = maquina.productos.cabeza
        while actual_producto:
            producto = actual_producto.valor
            producto_elem = ET.SubElement(listado_productos, "Producto")
            nombre_producto = ET.SubElement(producto_elem, "Nombre")
            nombre_producto.text = producto.nombre
            
            tiempo_total_elem = ET.SubElement(producto_elem, "TiempoTotal")
            tiempo_total_elem.text = str(producto.tiempo_total_ensamblaje)
            
            elaboracion_optima = ET.SubElement(producto_elem, "ElaboracionOptima")

            segundo_actual = 1
            while segundo_actual <= len(producto.historial_ensamblaje.segundos):
                acciones_segundo = producto.historial_ensamblaje.obtener_acciones_por_segundo(segundo_actual)
                
                tiempo_elem = ET.SubElement(elaboracion_optima, "Tiempo", NoSegundo=str(segundo_actual))

                if acciones_segundo:
                    accion_actual = acciones_segundo.cabeza
                    while accion_actual:
                        linea_ensamblaje_elem = ET.SubElement(tiempo_elem, "LineaEnsamblaje", NoLinea=str(segundo_actual))
                        linea_ensamblaje_elem.text = accion_actual.valor
                        accion_actual = accion_actual.siguiente
                
                segundo_actual += 1

            actual_producto = actual_producto.siguiente

        actual_maquina = actual_maquina.siguiente

    tree = ET.ElementTree(root)
    tree.write(ruta_salida_xml, encoding="utf-8", xml_declaration=True)
    print(f"Archivo de salida guardado en {ruta_salida_xml}")