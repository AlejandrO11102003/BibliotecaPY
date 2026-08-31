import pytest
from app import create_app, db
from app.models import Libro, Usuario

@pytest.fixture
def app_instance():
    app = create_app()
    
    # Para test, sobrescribimos config bd
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False 
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    """Cliente de pruebas para hacer peticiones HTTP"""
    return app_instance.test_client()

def test_ruta_principal(client):
    """Verifica que la página principal cargue correctamente"""
    response = client.get('/')
    assert response.status_code in [200, 302]

def test_ruta_libros(client):
    """Verifica que el listado de libros funcione"""
    response = client.get('/libros')
    assert response.status_code in [200, 302]

def test_ruta_usuarios(client):
    """Verifica que el listado de usuarios funcione"""
    response = client.get('/usuarios')
    assert response.status_code in [200, 302]