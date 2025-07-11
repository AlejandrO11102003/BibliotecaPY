import os
from flask import current_app
from werkzeug.utils import secure_filename

class FileService:
    """Servicio pa manejar img """
    
    @staticmethod
    def save_image(file, folder='img'):
        if not file:
            return None
        
        filename = secure_filename(file.filename)
        if not filename:
            return None
            
        # Crear el directorio si no existe
        upload_path = os.path.join(current_app.root_path, 'static', folder)
        os.makedirs(upload_path, exist_ok=True)
        
        # Guardar el archivo
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        return filename
    
    @staticmethod
    def delete_image(filename, folder='img'):
        if not filename:
            return False
            
        file_path = os.path.join(current_app.root_path, 'static', folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False 