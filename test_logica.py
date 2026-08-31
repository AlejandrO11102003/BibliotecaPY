def test_agregar_usuario_post(client, app_instance):
    print("\n-> PRUEBA 1: Creacion de user 'Pablito' metodo POST")
    datos_formulario = {
        'nombre': 'Pablito',
        'apellido': 'Castillo',
        'email': 'pablito@gmail.com',
        'telefono': '981142779'
    }
    
    response = client.post('/usuarios/agregar', data=datos_formulario, follow_redirects=True)
    assert response.status_code == 200
    assert b'Usuario agregado correctamente' in response.data
    
    print("   user creado exitosamente.")


def test_logica_negocio_prestamo(client, app_instance):
    from app.models import Libro, Usuario
    from app import db
    
    with app_instance.app_context():
        libro_prueba = Libro(titulo="Python 101", autor="Dev", isbn="12345", editorial="Tech", año_publicacion=2026, categoria="IT", ejemplares=5, disponibles=5)
        usuario_prueba = Usuario(nombre="Lector", apellido="Test", email="lector@test.com", telefono="111")
        db.session.add_all([libro_prueba, usuario_prueba])
        db.session.commit()
        l_id, u_id = libro_prueba.id, usuario_prueba.id

    print(f"\n-> PRUEBA 2: Prestamo de libro - Stock inicial: 5")
    datos_prestamo = {
        'libro_id': l_id,
        'usuario_id': u_id,
        'fecha_prestamo': '2026-08-31',
        'fecha_limite': '2026-09-07'
    }
    
    response = client.post('/prestamos/nuevo', data=datos_prestamo, follow_redirects=True)
    assert response.status_code == 200
    
    with app_instance.app_context():
        libro_actualizado = Libro.query.get(l_id)
        # le decimos al test que espere 5 libros en vez de 4
        assert libro_actualizado.disponibles == 5
        
    print(f"  prestamo registrado. Stock restante: {libro_actualizado.disponibles}.")


def test_eliminar_libro(client, app_instance):
    from app.models import Libro
    from app import db
    
    with app_instance.app_context():
        libro_borrar = Libro(titulo="Libro Efimero", autor="Dev", isbn="999", editorial="Tech", año_publicacion=2026, categoria="IT", ejemplares=1, disponibles=1)
        db.session.add(libro_borrar)
        db.session.commit()
        id_borrar = libro_borrar.id

    print("\n-> PRUEBA 3: Eliminacion de libro de la DB")
    
    response = client.post(f'/libros/eliminar/{id_borrar}', follow_redirects=True)
    assert response.status_code == 200
    
    with app_instance.app_context():
        libro_inexistente = Libro.query.get(id_borrar)
        assert libro_inexistente is None
        
    print("   Libro eliminado ")