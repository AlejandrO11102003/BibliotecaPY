from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Libro, Usuario, Prestamo
from app.forms import LibroForm, UsuarioForm, PrestamoForm, DevolucionForm
from datetime import datetime, timedelta


from sqlalchemy import func
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# Rutas para Libros
@main_bp.route('/libros')
def listar_libros():
    libros = Libro.query.all()
    return render_template('libros/listar.html', libros=libros)

@main_bp.route('/libros/agregar', methods=['GET', 'POST'])
def agregar_libro():
    form = LibroForm()
    if form.validate_on_submit():
        libro = Libro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            isbn=form.isbn.data,
            editorial=form.editorial.data,
            año_publicacion=form.año_publicacion.data,
            categoria=form.categoria.data,
            ejemplares=form.ejemplares.data,
            disponibles=form.disponibles.data
        )
        db.session.add(libro)
        db.session.commit()
        flash('Libro agregado correctamente', 'success')
        return redirect(url_for('main.listar_libros'))
    return render_template('libros/agregar.html', form=form)

@main_bp.route('/libros/editar/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    libro = Libro.query.get_or_404(id)
    form = LibroForm(obj=libro)
    if form.validate_on_submit():
        form.populate_obj(libro)
        db.session.commit()
        flash('Libro actualizado correctamente', 'success')
        return redirect(url_for('main.listar_libros'))
    return render_template('libros/editar.html', form=form, libro=libro)

#para eliminar libros

@main_bp.route('/libros/eliminar/<int:id>', methods=['POST'])
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)
    
    # Verificar si el libro tiene préstamos activos
    if Prestamo.query.filter_by(libro_id=id, estado='activo').count() > 0:
        flash('No se puede eliminar el libro porque tiene préstamos activos', 'danger')
        return redirect(url_for('main.listar_libros'))
    
    try:
        # Eliminar primero los préstamos relacionados (históricos)
        Prestamo.query.filter_by(libro_id=id).delete()
        db.session.delete(libro)
        db.session.commit()
        flash('Libro eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el libro: {str(e)}', 'danger')
    
    return redirect(url_for('main.listar_libros'))

# Rutas para Usuarios (similares a las de libros)
@main_bp.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@main_bp.route('/usuarios/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    form = UsuarioForm()
    if form.validate_on_submit():
        usuario = Usuario(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario agregado correctamente', 'success')
        return redirect(url_for('main.listar_usuarios'))
    return render_template('usuarios/agregar.html', form=form)

@main_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        form.populate_obj(usuario)
        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('main.listar_usuarios'))
    return render_template('usuarios/editar.html', form=form,usuario=usuario )



@main_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    # 🔍 Verifica si tiene algún préstamo activo
    prestamos_activos = Prestamo.query.filter_by(usuario_id=id, estado='activo').count()

    if prestamos_activos > 0:
        flash('No se puede eliminar el usuario porque tiene préstamos activos', 'danger')
        return redirect(url_for('main.listar_usuarios'))

    try:
        # ❌ Eliminar al usuario (y sus préstamos si configuraste cascade)
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el usuario', 'danger')

    return redirect(url_for('main.listar_usuarios'))

# Rutas para Préstamos
@main_bp.route('/prestamos')
def listar_prestamos():
    prestamos = Prestamo.query.all()
    return render_template('prestamos/listar.html', prestamos=prestamos,
                         datetime=datetime)

@main_bp.route('/prestamos/nuevo', methods=['GET', 'POST'])
def nuevo_prestamo():
    form = PrestamoForm()
    # Obtener libros disponibles y usuarios activos
    form.libro_id.choices = [(l.id, f"{l.titulo} - {l.autor}") 
                           for l in Libro.query.filter(Libro.disponibles > 0).all()]
    form.usuario_id.choices = [(u.id, f"{u.nombre} {u.apellido}") 
                             for u in Usuario.query.all()]
    
    if form.validate_on_submit():
        libro = Libro.query.get(form.libro_id.data)
        if libro.disponibles <= 0:
            flash('No hay ejemplares disponibles de este libro', 'danger')
            return redirect(url_for('main.nuevo_prestamo'))
        
        prestamo = Prestamo(
            libro_id=form.libro_id.data,
            usuario_id=form.usuario_id.data,
            fecha_prestamo=form.fecha_prestamo.data,
            fecha_limite=form.fecha_limite.data
        )
        
        libro.disponibles -= 1
        db.session.add(prestamo)
        db.session.commit()
        flash('Préstamo registrado correctamente', 'success')
        return redirect(url_for('main.listar_prestamos'))
    
    return render_template('prestamos/nuevo.html', form=form)

@main_bp.route('/prestamos/devolver/<int:id>', methods=['GET', 'POST'])
def devolver_prestamo(id):
    prestamo = Prestamo.query.get_or_404(id)
    form = DevolucionForm()
    
    if form.validate_on_submit():
        prestamo.fecha_devolucion = form.fecha_devolucion.data
        prestamo.estado = 'devuelto'
        
        libro = Libro.query.get(prestamo.libro_id)
        libro.disponibles += 1
        
        db.session.commit()
        flash('Devolución registrada correctamente', 'success')
        return redirect(url_for('main.listar_prestamos'))
    
    form.fecha_devolucion.data = datetime.today()
    return render_template('prestamos/devolver.html', form=form, prestamo=prestamo)

# Rutas para Reportes
@main_bp.route('/reportes')
def generar_reportes():
    total_libros = Libro.query.count()
    total_usuarios = Usuario.query.count()
    prestamos_activos = Prestamo.query.filter_by(estado='activo').count()
    prestamos_devueltos=Prestamo.query.filter_by(estado='devuelto').count()
    prestamos_vencidos = Prestamo.query.filter(
        Prestamo.fecha_limite < datetime.utcnow(),
        Prestamo.estado == 'activo'
    ).count()
    prestamos_recientes = Prestamo.query.order_by(Prestamo.fecha_prestamo.desc()).limit(5).all()
    
    # Obtener los 5 libros más prestados
    libros_populares = db.session.query(
        Libro.titulo,
        func.count(Prestamo.id).label('total_prestamos')
    ).join(Prestamo, Libro.id == Prestamo.libro_id)\
     .group_by(Libro.id)\
     .order_by(func.count(Prestamo.id).desc())\
     .limit(5).all()
    
    # Preparar datos para el gráfico
    labels = [libro.titulo[:20] + '...' if len(libro.titulo) > 20 else libro.titulo for libro in libros_populares]
    data = [libro.total_prestamos for libro in libros_populares]
    
    return render_template('reportes/generar.html', 
                         total_libros=total_libros,
                         total_usuarios=total_usuarios,
                         prestamos_activos=prestamos_activos,
                         prestamos_devueltos=prestamos_devueltos,
                         prestamos_vencidos=prestamos_vencidos,
                         prestamos_recientes=prestamos_recientes,
                         libros_labels=labels,
                         libros_data=data,
                         datetime=datetime)