import pandas as pd
import io
import json

def exportar_prestamos_a_excel(prestamos):
    data = []
    for p in prestamos:
        data.append({
            'Usuario': getattr(p.usuario, 'nombre', ''),
            'Libro': getattr(p.libro, 'titulo', ''),
            'Fecha Préstamo': getattr(p, 'fecha_prestamo', ''),
            'Fecha Devolución': getattr(p, 'fecha_devolucion', ''),
            'Estado': getattr(p, 'estado', '')
        })
    df = pd.DataFrame(data)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

def exportar_reporte_completo_a_excel(resumen, libros_populares, prestamos_recientes):
    # convertir resumen a dataframe
    resumen_df = pd.DataFrame([resumen])

    # convertir libros populares a json para pandas y luego a dataframe
    libros_json = json.dumps([
        {
            'Título': getattr(libro, 'titulo', ''),
            'Total de Préstamos': getattr(libro, 'total_prestamos', 0)
        }
        for libro in libros_populares
    ])
    libros_df = pd.read_json(libros_json)

    # convertir el diccionario a json para pandas  y luego a dataframe
    prestamos_json = json.dumps([
        {
            'Libro': getattr(p, 'libro', None).titulo if getattr(p, 'libro', None) else '',
            'Usuario': f"{getattr(p, 'usuario', None).nombre if getattr(p, 'usuario', None) else ''} {getattr(p, 'usuario', None).apellido if getattr(p, 'usuario', None) else ''}",
            'Fecha Préstamo': p.fecha_prestamo.strftime('%d/%m/%Y') if getattr(p, 'fecha_prestamo', None) else '',
            'Fecha Límite': p.fecha_limite.strftime('%d/%m/%Y') if getattr(p, 'fecha_limite', None) else '',
            'Estado': getattr(p, 'estado', '')
        }
        for p in prestamos_recientes
    ])
    prestamos_df = pd.read_json(prestamos_json)

    # crear el excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        resumen_df.to_excel(writer, sheet_name='Resumen', index=False)
        libros_df.to_excel(writer, sheet_name='Libros Populares', index=False)
        prestamos_df.to_excel(writer, sheet_name='Préstamos Recientes', index=False)
    output.seek(0)
    return output 