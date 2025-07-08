from datetime import datetime, timedelta
from app import db

class Libro(db.Model):
    
    __tablename__ = 'libros' 
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    editorial = db.Column(db.String(100))
    año_publicacion = db.Column(db.Integer)
    categoria = db.Column(db.String(50))
    ejemplares = db.Column(db.Integer, default=1)
    disponibles = db.Column(db.Integer, default=1)
    prestamos = db.relationship('Prestamo', backref='libro', lazy=True)

    def __repr__(self):
        return f'<Libro {self.titulo}>'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    prestamos = db.relationship('Prestamo', backref='usuario', cascade='all, delete', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nombre} {self.apellido}>'

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_devolucion = db.Column(db.DateTime)
    fecha_limite = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=14))
    estado = db.Column(db.String(20), default='activo')

    def __repr__(self):
        return f'<Prestamo {self.id}>'