def test_ruta_principal(client):
    response = client.get('/')
    assert response.status_code in [200, 302]

def test_ruta_libros(client):
    response = client.get('/libros')
    assert response.status_code in [200, 302]

def test_ruta_usuarios(client):
    response = client.get('/usuarios')
    assert response.status_code in [200, 302]