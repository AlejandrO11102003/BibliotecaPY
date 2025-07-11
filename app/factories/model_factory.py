from datetime import datetime
from app.services.file_service import FileService

class ModelFactory:
    """Factory para crear objetos de modelo desde formularios"""
    
    @staticmethod
    def create_libro_from_form(form, imagen_file=None):
        """Crea un diccionario de datos para libro desde formulario"""
        libro_data = {
            'titulo': form.titulo.data,
            'autor': form.autor.data,
            'isbn': form.isbn.data,
            'editorial': form.editorial.data,
            'año_publicacion': form.año_publicacion.data,
            'categoria': form.categoria.data,
            'ejemplares': form.ejemplares.data,
            'disponibles': form.disponibles.data,
            'imagen': None
        }
        
        # Manejar imagen si se proporciona
        if imagen_file:
            libro_data['imagen'] = FileService.save_image(imagen_file)
        
        return libro_data
    
    @staticmethod
    def create_usuario_from_form(form):
        """Crea un diccionario de datos para usuario desde formulario"""
        return {
            'nombre': form.nombre.data,
            'apellido': form.apellido.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'direccion': form.direccion.data
        }
    
    @staticmethod
    def create_prestamo_from_form(form):
        """Crea un diccionario de datos para préstamo desde formulario"""
        return {
            'libro_id': form.libro_id.data,
            'usuario_id': form.usuario_id.data,
            'fecha_prestamo': form.fecha_prestamo.data,
            'fecha_limite': form.fecha_limite.data,
            'estado': 'activo'
        }
    
    @staticmethod
    def update_libro_from_form(libro, form):
        """Actualiza un libro desde formulario"""
        return {
            'titulo': form.titulo.data,
            'autor': form.autor.data,
            'isbn': form.isbn.data,
            'editorial': form.editorial.data,
            'año_publicacion': form.año_publicacion.data,
            'categoria': form.categoria.data,
            'ejemplares': form.ejemplares.data,
            'disponibles': form.disponibles.data
        }
    
    @staticmethod
    def update_usuario_from_form(usuario, form):
        """Actualiza un usuario desde formulario"""
        return {
            'nombre': form.nombre.data,
            'apellido': form.apellido.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'direccion': form.direccion.data
        }
    
    @staticmethod
    def create_choices_for_select(items, id_field='id', display_field='nombre'):
        """Crea opciones para campos SelectField"""
        choices = []
        for item in items:
            if hasattr(item, display_field):
                display_value = getattr(item, display_field)
                if hasattr(item, 'apellido'):  # Para usuarios
                    display_value = f"{item.nombre} {item.apellido}"
                elif hasattr(item, 'autor'):   # Para libros
                    display_value = f"{item.titulo} - {item.autor}"
                choices.append((getattr(item, id_field), display_value))
        return choices 