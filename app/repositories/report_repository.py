from app import db
from app.models import Libro, Usuario, Prestamo
from datetime import datetime
from sqlalchemy import func

# Repositorio para manejar consultas de reportes y estadísticas
class ReportRepository:
    
    def get_total_libros(self):
        # Obtener total de libros
        return Libro.query.count()
    
    def get_total_usuarios(self):
        # Obtener total de usuarios
        return Usuario.query.count()
    
    def get_prestamos_activos(self):
        # Obtener total de préstamos activos
        return Prestamo.query.filter_by(estado='activo').count()
    
    def get_prestamos_devueltos(self):
        # Obtener total de préstamos devueltos
        return Prestamo.query.filter_by(estado='devuelto').count()
    
    def get_prestamos_vencidos(self):
        # Obtener total de préstamos vencidos
        return Prestamo.query.filter(
            Prestamo.fecha_limite < datetime.utcnow(),
            Prestamo.estado == 'activo'
        ).count()
    
    def get_prestamos_recientes(self, limit=5):
        # Obtener préstamos más recientes
        return Prestamo.query.order_by(Prestamo.fecha_prestamo.desc()).limit(limit).all()
    
    def get_libros_populares(self, limit=5):
        # Obtener los libros más prestados
        return db.session.query(
            Libro.titulo,
            func.count(Prestamo.id).label('total_prestamos')
        ).join(Prestamo, Libro.id == Prestamo.libro_id)\
         .group_by(Libro.id)\
         .order_by(func.count(Prestamo.id).desc())\
         .limit(limit).all()
    
    def get_estadisticas_completas(self):
        # Obtener todas las estadísticas en un solo método
        return {
            'total_libros': self.get_total_libros(),
            'total_usuarios': self.get_total_usuarios(),
            'prestamos_activos': self.get_prestamos_activos(),
            'prestamos_devueltos': self.get_prestamos_devueltos(),
            'prestamos_vencidos': self.get_prestamos_vencidos(),
            'prestamos_recientes': self.get_prestamos_recientes(),
            'libros_populares': self.get_libros_populares()
        } 