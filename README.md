# Sistema de Gestión de Biblioteca

Sistema web para la gestión de préstamos y devoluciones de libros, desarrollado con Flask y aplicando el patrón Repository.

##  Arquitectura


```
app/
├── __init__.py              # Configuración de la aplicación Flask
├── models.py               # Modelos de SQLAlchemy
├── forms.py                # Formularios WTForms
├── routes.py               # Rutas HTTP (controladores)
├── repositories/           # Patrón Repository
│   ├── libro_repository.py
│   ├── usuario_repository.py
│   ├── prestamo_repository.py
│   └── report_repository.py
├── services/               # Servicios específicos
│   └── file_service.py
├── factories/              # Patrón Factory
│   └── model_factory.py
├── static/                 # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
├── templates/              # Plantillas HTML
|───grafico_numpy.py    # Utilidades para gráficos
```

## 🎯 Principios SOLID Aplicados

### ✅ Single Responsibility Principle (SRP)
- **Repositories**: Cada repositorio maneja una entidad específica
- **Services**: Servicios especializados (ej: FileService para archivos)
- **Factories**: Creación centralizada de objetos desde formularios
- **Routes**: Solo manejo de HTTP y coordinación

### ✅ Open/Closed Principle (OCP)
- Los repositories están abiertos para extensión
- Fácil agregar nuevos métodos sin modificar código existente

### ✅ Interface Segregation Principle (ISP)
- Cada repositorio tiene métodos específicos para su entidad
- No hay dependencias innecesarias

### ✅ Dependency Inversion Principle (DIP)
- Las rutas dependen de abstracciones (repositories)
- Fácil cambiar implementaciones sin afectar el código

## 🚀 Funcionalidades

### 📚 Gestión de Libros
- Agregar, editar, eliminar libros
- Subida de imágenes de portada
- Control de inventario (ejemplares disponibles)

### 👥 Gestión de Usuarios
- Registro y edición de usuarios
- Validación de datos
- Control de préstamos activos

### 📖 Gestión de Préstamos
- Registrar nuevos préstamos
- Devolución de libros
- Control automático de disponibilidad
- Validación de fechas límite

### 📊 Reportes
- Estadísticas generales
- Libros más prestados
- Préstamos vencidos
- Gráficos generados con Matplotlib

## 🛠️ Tecnologías

- **Backend**: Flask, SQLAlchemy, WTForms
- **Base de Datos**: MySQL
- **Frontend**: Bootstrap 4, HTML5, CSS3, JavaScript
- **Gráficos**: Matplotlib, NumPy
- **Patrones**: Repository Pattern

## 📦 Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/AlejandrO11102003/BibliotecaPY.git
cd BibliotecaPY
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos:**
```bash
python init_db.py
```

5. **Ejecutar la aplicación:**
```bash
python run.py
```

## 🔧 Configuración

Crear archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/biblioteca
```

## 📁 Estructura de Repositories y Factories

### ModelFactory
- `create_libro_from_form(form, imagen_file)`: Crear datos de libro desde formulario
- `create_usuario_from_form(form)`: Crear datos de usuario desde formulario
- `create_prestamo_from_form(form)`: Crear datos de préstamo desde formulario
- `update_libro_from_form(libro, form)`: Actualizar libro desde formulario
- `update_usuario_from_form(usuario, form)`: Actualizar usuario desde formulario
- `create_choices_for_select(items, id_field, display_field)`: Crear opciones para SelectField

## 📁 Estructura de Repositories

### LibroRepository
- `get_all()`: Obtener todos los libros
- `get_by_id(id)`: Obtener libro por ID
- `get_disponibles()`: Libros con ejemplares disponibles
- `create(libro_data)`: Crear nuevo libro
- `update(libro, form_data)`: Actualizar libro
- `delete(id)`: Eliminar libro
- `decrease_available(id)`: Disminuir disponibilidad
- `increase_available(id)`: Aumentar disponibilidad

### UsuarioRepository
- `get_all()`: Obtener todos los usuarios
- `get_by_id(id)`: Obtener usuario por ID
- `create(usuario_data)`: Crear nuevo usuario
- `update(usuario, form_data)`: Actualizar usuario
- `delete(id)`: Eliminar usuario
- `has_active_loans(id)`: Verificar préstamos activos

### PrestamoRepository
- `get_all()`: Obtener todos los préstamos
- `create(prestamo_data)`: Crear nuevo préstamo
- `devolver_prestamo(id, fecha)`: Marcar como devuelto
- `get_activos()`: Préstamos activos
- `get_vencidos()`: Préstamos vencidos
- `get_libros_populares()`: Libros más prestados

### ReportRepository
- `get_estadisticas_completas()`: Todas las estadísticas
- Métodos específicos para cada tipo de reporte

## 🎨 Características del Frontend

- **Diseño responsivo** con Bootstrap 4
- **Sidebar de navegación** fijo
- **Paleta de colores** personalizada (blanco y negro)
- **Tablas interactivas** con búsqueda
- **Formularios validados** con mensajes de error
- **Gráficos estadísticos** integrados

## 🔒 Seguridad

- Validación de formularios con WTForms
- Sanitización de nombres de archivos
- Control de acceso a archivos estáticos
- Manejo de errores con try-catch
- Validaciones de negocio en repositories

## 🧪 Mantenibilidad

- **Código modular** y bien organizado
- **Separación de responsabilidades** clara
- **Documentación** en cada método
- **Manejo de errores** centralizado
- **Fácil extensión** para nuevas funcionalidades

## 📈 Beneficios del Repository Pattern

1. **Testabilidad**: Fácil crear mocks para testing
2. **Mantenibilidad**: Cambios en BD no afectan lógica de negocio
3. **Reutilización**: Repositories se pueden usar en diferentes partes
4. **Escalabilidad**: Fácil agregar nuevas funcionalidades
5. **Legibilidad**: Código más limpio y organizado

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para nueva funcionalidad
3. Commit los cambios
4. Push a la rama
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
