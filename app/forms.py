from datetime import datetime, timedelta  # Asegúrate de importar timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed

class LibroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    autor = StringField('Autor', validators=[DataRequired(), Length(max=100)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(max=20)])
    editorial = StringField('Editorial', validators=[Length(max=100)])
    año_publicacion = IntegerField('Año de Publicación')
    categoria = StringField('Categoría', validators=[Length(max=50)])
    ejemplares = IntegerField('Ejemplares', validators=[DataRequired()])
    disponibles = IntegerField('Disponibles', validators=[DataRequired()])
    imagen = FileField('Imagen del libro', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imagenes!')])
    submit = SubmitField('Guardar')

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    direccion = StringField('Dirección', validators=[Length(max=200)])
    submit = SubmitField('Guardar')

class PrestamoForm(FlaskForm):
    libro_id = SelectField('Libro', coerce=int, validators=[DataRequired()])
    usuario_id = SelectField('Usuario', coerce=int, validators=[DataRequired()])
    fecha_prestamo = DateField('Fecha de Préstamo', format='%Y-%m-%d', default=datetime.today)
    fecha_limite = DateField('Fecha Límite', format='%Y-%m-%d', 
                        default=lambda: datetime.today() + timedelta(days=14))
    submit = SubmitField('Registrar Préstamo')

class DevolucionForm(FlaskForm):
    fecha_devolucion = DateField('Fecha de Devolución', format='%Y-%m-%d', default=datetime.today)
    submit = SubmitField('Registrar Devolución')