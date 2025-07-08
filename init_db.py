from app import create_app, db
from app.models import Libro, Usuario, Prestamo
from datetime import datetime, timedelta

app = create_app()

def init_db():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Verificar si ya hay datos
        if not Libro.query.first():
            # Libros de ejemplo
            libros = [
                Libro(
                    titulo="Cien años de soledad",
                    autor="Gabriel García Márquez",
                    isbn="9780307474728",
                    editorial="Sudamericana",
                    año_publicacion=1967,
                    categoria="Novela",
                    ejemplares=5,
                    disponibles=5
                ),
                Libro(
                    titulo="El principito",
                    autor="Antoine de Saint-Exupéry",
                    isbn="9780156013925",
                    editorial="Reynal & Hitchcock",
                    año_publicacion=1943,
                    categoria="Fábula",
                    ejemplares=3,
                    disponibles=3
                )
            ]
            
            # Usuarios de ejemplo
            usuarios = [
                Usuario(
                    nombre="Juan",
                    apellido="Pérez",
                    email="juan@example.com",
                    telefono="123456789"
                ),
                Usuario(
                    nombre="María",
                    apellido="Gómez",
                    email="maria@example.com",
                    telefono="987654321"
                )
            ]
            
            db.session.add_all(libros)
            db.session.add_all(usuarios)
            db.session.commit()
            
            print("Base de datos inicializada con datos de ejemplo")

if __name__ == '__main__':
    init_db()