from app import db
from app.models import Prestamo, Libro, Usuario
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

# Repositorio para manejar operaciones de base de datos relacionadas con Préstamos
class PrestamoRepository:
    
    def get_all(self):
        # Obtener todos los préstamos
        return Prestamo.query.all()
    
    def get_by_id(self, id):
        # Obtener un préstamo por ID
        return Prestamo.query.get_or_404(id)
    
    def create(self, prestamo_data):
        # Crear un nuevo préstamo
        try:
            # Verificar que el libro existe
            libro = Libro.query.get(prestamo_data.get('libro_id'))
            if not libro:
                raise ValueError(f'El libro con ID {prestamo_data.get("libro_id")} no existe')
            
            # Verificar que el usuario existe
            usuario = Usuario.query.get(prestamo_data.get('usuario_id'))
            if not usuario:
                raise ValueError(f'El usuario con ID {prestamo_data.get("usuario_id")} no existe')
            
            # Verificar que el libro tiene ejemplares disponibles
            if libro.disponibles <= 0:
                raise ValueError(f'No hay ejemplares disponibles del libro "{libro.titulo}"')
            
            prestamo = Prestamo(**prestamo_data)
            db.session.add(prestamo)
            db.session.commit()
            return prestamo
        except IntegrityError as e:
            db.session.rollback()
            if "foreign key" in str(e).lower():
                raise ValueError('Error: El libro o usuario especificado no existe')
            else:
                raise ValueError('Error de integridad en la base de datos')
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error al crear el préstamo: {str(e)}')
    
    def update(self, prestamo, form_data):
        # Actualizar un préstamo existente
        for field, value in form_data.items():
            if hasattr(prestamo, field):
                setattr(prestamo, field, value)
        db.session.commit()
        return prestamo
    
    def devolver_prestamo(self, id, fecha_devolucion):
        # Marcar un préstamo como devuelto
        try:
            prestamo = self.get_by_id(id)
            
            # Verificar que el préstamo no esté ya devuelto
            if prestamo.estado == 'devuelto':
                raise ValueError('Este préstamo ya ha sido devuelto')
            
            # Verificar que la fecha de devolución no sea anterior a la fecha de préstamo
            if fecha_devolucion < prestamo.fecha_prestamo.date():
                raise ValueError('La fecha de devolución no puede ser anterior a la fecha de préstamo')
            
            prestamo.fecha_devolucion = fecha_devolucion
            prestamo.estado = 'devuelto'
            db.session.commit()
            return prestamo
        except ValueError as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error al devolver el préstamo: {str(e)}')
    
    def get_activos(self):
        # Obtener préstamos activos
        return Prestamo.query.filter_by(estado='activo').all()
    
    def get_devueltos(self):
        # Obtener préstamos devueltos
        return Prestamo.query.filter_by(estado='devuelto').all()
    
    def get_vencidos(self):
        # Obtener préstamos vencidos
        return Prestamo.query.filter(
            Prestamo.fecha_limite < datetime.utcnow(),
            Prestamo.estado == 'activo'
        ).all()
    
    def get_recientes(self, limit=5):
        # Obtener préstamos más recientes
        return Prestamo.query.order_by(Prestamo.fecha_prestamo.desc()).limit(limit).all()
    
    def count_activos(self):
        # Contar préstamos activos
        return Prestamo.query.filter_by(estado='activo').count()
    
    def count_devueltos(self):
        # Contar préstamos devueltos
        return Prestamo.query.filter_by(estado='devuelto').count()
    
    def count_vencidos(self):
        # Contar préstamos vencidos
        return Prestamo.query.filter(
            Prestamo.fecha_limite < datetime.utcnow(),
            Prestamo.estado == 'activo'
        ).count()
    
    def get_libros_populares(self, limit=5):
        # Obtener los libros más prestados
        return db.session.query(
            Libro.titulo,
            func.count(Prestamo.id).label('total_prestamos')
        ).join(Prestamo, Libro.id == Prestamo.libro_id)\
        .group_by(Libro.id)\
        .order_by(func.count(Prestamo.id).desc())\
        .limit(limit).all() 