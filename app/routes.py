from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime, timedelta
import numpy as np
# repositorios
from app.repositories.libro_repository import LibroRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.prestamo_repository import PrestamoRepository
from app.repositories.report_repository import ReportRepository
# servicios
from app.services.file_service import FileService
# factory
from app.factories.model_factory import ModelFactory
# formularios
from app.forms import LibroForm, UsuarioForm, PrestamoForm, DevolucionForm
# util
from app.grafico_numpy import generar_grafico_libros_populares

main_bp = Blueprint('main', __name__)

# inicializar repositorios
libro_repo = LibroRepository()
usuario_repo = UsuarioRepository()
prestamo_repo = PrestamoRepository()
report_repo = ReportRepository()

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/libros')
def listar_libros():
    libros = libro_repo.get_all()
    return render_template('libros/listar.html', libros=libros)

@main_bp.route('/libros/agregar', methods=['GET', 'POST'])
def agregar_libro():
    form = LibroForm()
    if form.validate_on_submit():
        try:
            # patron factory para crear datos del libro
            libro_data = ModelFactory.create_libro_from_form(form, form.imagen.data)
            libro_repo.create(libro_data)
            flash('Libro agregado correctamente', 'success')
            return redirect(url_for('main.listar_libros'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
    return render_template('libros/agregar.html', form=form)

@main_bp.route('/libros/editar/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    libro = libro_repo.get_by_id(id)
    form = LibroForm(obj=libro)
    if form.validate_on_submit():
        try:
            # patron factory para actualizar datos del libro
            form_data = ModelFactory.update_libro_from_form(libro, form)
            libro_repo.update(libro, form_data)
            flash('Libro actualizado correctamente', 'success')
            return redirect(url_for('main.listar_libros'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
    return render_template('libros/editar.html', form=form, libro=libro)


@main_bp.route('/libros/eliminar/<int:id>', methods=['POST'])
def eliminar_libro(id):
    try:
        libro_repo.delete(id)
        flash('Libro eliminado correctamente', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(f'Error al eliminar el libro: {str(e)}', 'danger')
    
    return redirect(url_for('main.listar_libros'))

@main_bp.route('/usuarios')
def listar_usuarios():
    usuarios = usuario_repo.get_all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@main_bp.route('/usuarios/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        try:
            # patron factory para crear datos del usuario
            usuario_data = ModelFactory.create_usuario_from_form(form)
            usuario_repo.create(usuario_data)
            flash('Usuario agregado correctamente', 'success')
            return redirect(url_for('main.listar_usuarios'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
    return render_template('usuarios/agregar.html', form=form)

@main_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = usuario_repo.get_by_id(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        try:
            # patron factory para actualizar datos del usuario
            form_data = ModelFactory.update_usuario_from_form(usuario, form)
            usuario_repo.update(usuario, form_data)
            flash('Usuario actualizado correctamente', 'success')
            return redirect(url_for('main.listar_usuarios'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
    return render_template('usuarios/editar.html', form=form, usuario=usuario)


@main_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    try:
        usuario_repo.delete(id)
        flash('Usuario eliminado correctamente', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash('Error al eliminar el usuario', 'danger')

    return redirect(url_for('main.listar_usuarios'))

@main_bp.route('/prestamos')
def listar_prestamos():
    prestamos = prestamo_repo.get_all()
    return render_template('prestamos/listar.html', prestamos=prestamos,
                        datetime=datetime)

@main_bp.route('/prestamos/nuevo', methods=['GET', 'POST'])
def nuevo_prestamo():
    form = PrestamoForm()
    form.libro_id.choices = ModelFactory.create_choices_for_select(
        libro_repo.get_disponibles(), 'id', 'titulo'
    )
    form.usuario_id.choices = ModelFactory.create_choices_for_select(
        usuario_repo.get_all(), 'id', 'nombre'
    )
    
    if form.validate_on_submit():
        try:
            prestamo_data = ModelFactory.create_prestamo_from_form(form)
            prestamo_repo.create(prestamo_data)
            # Disminuir disponibilidad después de crear el préstamo exitosamente
            libro_repo.decrease_available(form.libro_id.data)
            flash('Préstamo registrado correctamente', 'success')
            return redirect(url_for('main.listar_prestamos'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
    
    return render_template('prestamos/nuevo.html', form=form)

@main_bp.route('/prestamos/devolver/<int:id>', methods=['GET', 'POST'])
def devolver_prestamo(id):
    prestamo = prestamo_repo.get_by_id(id)
    form = DevolucionForm()
    
    if form.validate_on_submit():
        try:
            # setear prestamo como devuelto
            prestamo_repo.devolver_prestamo(id, form.fecha_devolucion.data)
            
            # aumentar ejemplares disponibles
            libro_repo.increase_available(prestamo.libro_id)
            flash('Devolución registrada correctamente', 'success')
            return redirect(url_for('main.listar_prestamos'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
    
    form.fecha_devolucion.data = datetime.today()
    return render_template('prestamos/devolver.html', form=form, prestamo=prestamo)

@main_bp.route('/reportes')
def generar_reportes():
    # traer estadísticas completas
    stats = report_repo.get_estadisticas_completas()
    # mandar estadísticas a la plantilla
    libros_populares = stats['libros_populares']
    labels = [libro.titulo[:20] + '...' if len(libro.titulo) > 20 else libro.titulo for libro in libros_populares]
    data = np.array([libro.total_prestamos for libro in libros_populares])

    # generar img del gráfico de libros populares
    image_base64 = generar_grafico_libros_populares(libros_populares)

    return render_template('reportes/generar.html', 
                        total_libros=stats['total_libros'],
                        total_usuarios=stats['total_usuarios'],
                        prestamos_activos=stats['prestamos_activos'],
                        prestamos_devueltos=stats['prestamos_devueltos'],
                        prestamos_vencidos=stats['prestamos_vencidos'],
                        prestamos_recientes=stats['prestamos_recientes'],
                        libros_labels=labels,
                        libros_data=data.tolist(),
                        datetime=datetime,
                        image_base64=image_base64
                        )