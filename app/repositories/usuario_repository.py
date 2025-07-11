from app import db
from app.models import Usuario, Prestamo
from sqlalchemy.exc import IntegrityError

# Repositorio para manejar operaciones de base de datos relacionadas con Usuarios
class UsuarioRepository:
    
    def get_all(self):
        # Obtener todos los usuarios
        return Usuario.query.all()
    
    def get_by_id(self, id):
        # Obtener un usuario por ID
        return Usuario.query.get_or_404(id)
    
    def create(self, usuario_data):
        # Crear un nuevo usuario
        try:
            usuario = Usuario(**usuario_data)
            db.session.add(usuario)
            db.session.commit()
            return usuario
        except IntegrityError as e:
            db.session.rollback()
            # Verificar si es error de email duplicado
            if "email" in str(e).lower():
                raise ValueError(f'Ya existe un usuario con el email: {usuario_data.get("email")}')
            else:
                raise ValueError('Error de integridad en la base de datos')
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error al crear el usuario: {str(e)}')
    
    def update(self, usuario, form_data):
        # Actualizar un usuario existente
        try:
            for field, value in form_data.items():
                if hasattr(usuario, field):
                    setattr(usuario, field, value)
            db.session.commit()
            return usuario
        except IntegrityError as e:
            db.session.rollback()
            # Verificar si es error de email duplicado
            if "email" in str(e).lower():
                raise ValueError(f'Ya existe un usuario con el email: {form_data.get("email")}')
            else:
                raise ValueError('Error de integridad en la base de datos')
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Error al actualizar el usuario: {str(e)}')
    
    def delete(self, id):
        # Eliminar un usuario
        usuario = self.get_by_id(id)
        
        # Verificar si tiene préstamos activos
        if Prestamo.query.filter_by(usuario_id=id, estado='activo').count() > 0:
            raise ValueError('No se puede eliminar el usuario porque tiene préstamos activos')
        
        try:
            db.session.delete(usuario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def has_active_loans(self, id):
        # Verificar si un usuario tiene préstamos activos
        return Prestamo.query.filter_by(usuario_id=id, estado='activo').count() > 0
    
    def count(self):
        # Contar total de usuarios
        return Usuario.query.count() 