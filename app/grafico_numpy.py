import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def generar_grafico_libros_populares(libros_populares):
    labels = [libro.titulo[:20] + '...' if len(libro.titulo) > 20 else libro.titulo for libro in libros_populares]
    data = np.array([libro.total_prestamos for libro in libros_populares])

    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(labels, data, color='skyblue')
    ax.set_ylabel('Préstamos')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return image_base64 