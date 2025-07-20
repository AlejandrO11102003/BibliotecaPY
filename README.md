# Sistema de Gestión de Biblioteca

Sistema web para la gestión de préstamos y devoluciones de libros, desarrollado con Flask, SQLAlchemy y el patrón Repository. **Actualmente solo usa MySQL como base de datos.**

---

## 🚦 Estado del Proyecto

- **Base de datos en uso:** MySQL (NO se usa SQLite, puedes eliminar cualquier archivo `app.db` y líneas comentadas de SQLite)
- **Inicialización de datos:** El script `init_db.py` es solo para poblar la base de datos con datos de ejemplo, no es obligatorio para correr la app.
- **Variables de entorno:** Se recomienda usar `.env` para la clave secreta y, opcionalmente, la URI de la base de datos.
- **Exportación de reportes:** Se puede exportar información a Excel usando pandas (`app/pandas.py`).
- **Archivos no usados:** `app/utils.py` (vacío), archivos JSON en `app/data/` (vacíos), SQLite.

---

## 🗂️ Estructura del Proyecto

```
Prestamos-De-Libros/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── grafico_numpy.py
│   ├── pandas.py
│   ├── data/
│   │   ├── libros.json (vacío)
│   │   ├── prestamos.json (vacío)
│   │   └── usuarios.json (vacío)
│   ├── factories/
│   │   └── model_factory.py
│   ├── repositories/
│   │   ├── libro_repository.py
│   │   ├── usuario_repository.py
│   │   ├── prestamo_repository.py
│   │   └── report_repository.py
│   ├── services/
│   │   └── file_service.py
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── scripts.js
│   │   └── img/
│   │       ├── 04.png
│   │       ├── ChatGPT_Image_19_jun_2025_12_45_15.png
│   │       └── imgalejadnro.jpg
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── libros/
│   │   │   ├── agregar.html
│   │   │   ├── editar.html
│   │   │   └── listar.html
│   │   ├── usuarios/
│   │   │   ├── agregar.html
│   │   │   ├── editar.html
│   │   │   └── listar.html
│   │   ├── prestamos/
│   │   │   ├── devolver.html
│   │   │   ├── listar.html
│   │   │   └── nuevo.html
│   │   └── reportes/
│   │       └── generar.html
├── config.py
├── init_db.py
├── requirements.txt
├── run.py
└── README.md
```

---

## 🛠️ Tecnologías

- **Backend:** Flask, SQLAlchemy, Flask-Migrate, WTForms
- **Base de Datos:** MySQL (con PyMySQL)
- **Frontend:** Bootstrap 4, HTML5, CSS3, JavaScript
- **Gráficos:** Matplotlib, NumPy, pandas (para exportar a Excel)
- **Patrones:** Repository Pattern, Factory

---

## 🚀 Funcionalidades

- Gestión de Libros: agregar, editar, eliminar, subir imágenes, control de inventario.
- Gestión de Usuarios: registro, edición, validación, control de préstamos activos.
- Gestión de Préstamos: registrar, devolver, control de disponibilidad, validación de fechas.
- Reportes: estadísticas, libros más prestados, préstamos vencidos, gráficos y exportación a Excel.

---

## 📦 Instalación y Puesta en Marcha

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/AlejandrO11102003/BibliotecaPY.git
   cd BibliotecaPY
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos MySQL:**
   - Crea una base de datos llamada `biblioteca` en tu servidor MySQL.
   - Ajusta el usuario y contraseña en `config.py` o usando variables de entorno (ver abajo).

5. **Inicializa la base de datos con datos de ejemplo (opcional):**
   - Solo si quieres poblarla con datos de ejemplo:
   ```bash
   python init_db.py
   ```
   - Este paso es manual y solo necesario la primera vez o si quieres reiniciar la base de datos.

6. **Ejecuta la aplicación:**
   ```bash
   python run.py
   ```

---

## 🔧 Configuración

Puedes usar variables de entorno para mayor seguridad y flexibilidad. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```env
SECRET_KEY=tu-clave-secreta-aqui
# Si quieres usar variable de entorno para la base de datos:
# DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/biblioteca
```
Por defecto, la conexión a MySQL está definida en `config.py`. Si prefieres usar la variable de entorno `DATABASE_URL`, descomenta y ajusta la línea correspondiente en `config.py`.

---

## 📁 Estructura de Repositories y Factories

### ModelFactory
- `create_libro_from_form(form, imagen_file)`: Crear datos de libro desde formulario
- `create_usuario_from_form(form)`: Crear datos de usuario desde formulario
- `create_prestamo_from_form(form)`: Crear datos de préstamo desde formulario
- `update_libro_from_form(libro, form)`: Actualizar libro desde formulario
- `update_usuario_from_form(usuario, form)`: Actualizar usuario desde formulario
- `create_choices_for_select(items, id_field, display_field)`: Crear opciones para SelectField

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

---

## 📊 Exportación de Reportes a Excel

El archivo `app/pandas.py` permite exportar:
- Listados de préstamos a Excel (`exportar_prestamos_a_excel`)
- Reportes completos con varias hojas (resumen, libros populares, préstamos recientes) a Excel (`exportar_reporte_completo_a_excel`)

Esto facilita la generación de reportes avanzados para análisis o impresión.

---

## 🎨 Características del Frontend

- Diseño responsivo con Bootstrap 4
- Sidebar de navegación fijo
- Paleta de colores personalizada (blanco y negro)
- Tablas interactivas con búsqueda
- Formularios validados con mensajes de error
- Gráficos estadísticos integrados

---

## 🔒 Seguridad

- Validación de formularios con WTForms
- Sanitización de nombres de archivos
- Control de acceso a archivos estáticos
- Manejo de errores con try-catch
- Validaciones de negocio en repositories

---

## 🧪 Mantenibilidad

- Código modular y bien organizado
- Separación de responsabilidades clara
- Documentación en cada método
- Manejo de errores centralizado
- Fácil extensión para nuevas funcionalidades

---

## 📈 Beneficios del Repository Pattern

1. Testabilidad: Fácil crear mocks para testing
2. Mantenibilidad: Cambios en BD no afectan lógica de negocio
3. Reutilización: Repositories se pueden usar en diferentes partes
4. Escalabilidad: Fácil agregar nuevas funcionalidades
5. Legibilidad: Código más limpio y organizado

---

## ⚠️ Notas y Limpieza

- **No uses ni mantengas archivos `app.db` ni configuraciones de SQLite.**
- El script `init_db.py` es solo para inicialización manual, no es obligatorio para correr la app.
- Usa variables de entorno para mayor seguridad.
- Puedes eliminar `app/utils.py` y los archivos JSON vacíos en `app/data/` si no los necesitas.

---

## 🤝 Contribuir

1. Haz fork del proyecto
2. Crea una rama para tu funcionalidad
3. Haz commit de tus cambios
4. Haz push a la rama
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
