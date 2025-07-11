from app import db
from app.models import Libro, Prestamo
from sqlalchemy.exc import IntegrityError

# Repositorio para manejar operaciones de base de datos relacionadas con Libros
class LibroRepository:
    
    def get_all(self):
        # Obtener todos los libros
        return Libro.query.all()
    
    def get_by_id(self, id):
        # Obtener un libro por ID
        return Libro.query.get_or_404(id)
    
    def get_disponibles(self):
        # Obtener libros con ejemplares disponibles
        return Libro.query.filter(Libro.disponibles > 0).all()
    
    def create(self, libro_data):
        # Crear un nuevo libro
        try:
            libro = Libro(**libro_data)
            db.session.add(libro)
            db.session.commit()
            return libro
        except IntegrityError as e:
            db.session.rollback()
            # Verificar si es error de ISBN duplicado
            if "isbn" in str(e).lower():
                raise ValueError(f'Ya existe un libro con el ISBN: {libro_data.get("isbn")}')
            # Verificar si es error de título duplicado (si tuvieras esa restricción)
            elif "titulo" in str(e).lower():
                raise ValueError(f'Ya existe un libro con el título: {libro_data.get("titulo")}')
            else:
                raise ValueError('Error de integridad en la base de datos')
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error al crear el libro: {str(e)}')
    
    def update(self, libro, form_data):
        # Actualizar un libro existente
        try:
            for field, value in form_data.items():
                if hasattr(libro, field):
                    setattr(libro, field, value)
            db.session.commit()
            return libro
        except IntegrityError as e:
            db.session.rollback()
            # Verificar si es error de ISBN duplicado
            if "isbn" in str(e).lower():
                raise ValueError(f'Ya existe un libro con el ISBN: {form_data.get("isbn")}')
            else:
                raise ValueError('Error de integridad en la base de datos')
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error al actualizar el libro: {str(e)}')
    
    def delete(self, id):
        # Eliminar un libro
        libro = self.get_by_id(id)
        
        # Verificar si el libro tiene préstamos activos
        if Prestamo.query.filter_by(libro_id=id, estado='activo').count() > 0:
            raise ValueError('No se puede eliminar el libro porque tiene préstamos activos')
        
        try:
            # Eliminar primero los préstamos relacionados (históricos)
            Prestamo.query.filter_by(libro_id=id).delete()
            db.session.delete(libro)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def has_active_loans(self, id):
        # Verificar si un libro tiene préstamos activos
        return Prestamo.query.filter_by(libro_id=id, estado='activo').count() > 0
    
    def decrease_available(self, id):
        # Disminuir el número de ejemplares disponibles
        libro = self.get_by_id(id)
        if libro.disponibles > 0:
            libro.disponibles -= 1
            db.session.commit()
            return True
        return False
    
    def increase_available(self, id):
        # Aumentar el número de ejemplares disponibles
        libro = self.get_by_id(id)
        libro.disponibles += 1
        db.session.commit()
        return True 