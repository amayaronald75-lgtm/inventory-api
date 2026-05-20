# inventory-api

API desarrollada con FastAPI para la gestión de inventario de un local, permitiendo administrar usuarios, autenticación, categorías y productos con validaciones básicas de negocio.

## 🚀 Características

- Registro de usuarios
- Inicio de sesión con token JWT
- Hash seguro de contraseñas con `bcrypt`
- CRUD de categorías
- CRUD de productos
- Relación entre categorías y productos
- Filtros de productos por categoría, nombre y precio
- Ordenamiento y paginación básica
- Base de datos SQLite con SQLAlchemy ORM

## 🛠️ Tecnologías usadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Bcrypt
- Python-Jose

## 🧩 Estructura del proyecto

```text
inventory_api/
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── inventory.db
├── .gitignore
├── routers/
│   ├── __init__.py
│   ├── categories.py
│   └── products.py
└── README.md
```

## 🔧 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/amayaronald75-lgtm/inventory-api.git
cd inventory-api
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
```

En Windows:

```bash
venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install fastapi uvicorn sqlalchemy bcrypt python-jose
```

## ⚙️ Ejecución

Ejecuta el servidor desde la raíz del proyecto:

```bash
uvicorn main:app --reload
```

Si el puerto por defecto está ocupado, puedes usar otro:

```bash
uvicorn main:app --reload --port 8003
```

Luego abre en el navegador:

- Documentación Swagger: `http://127.0.0.1:8000/docs`
- Documentación Redoc: `http://127.0.0.1:8000/redoc`

## ✅ Autenticación

El proyecto utiliza JWT para el manejo de sesiones de usuario.

### 🔀 Flujo básico

1. Crear un usuario en `POST /users`
2. Iniciar sesión en `POST /login`
3. Obtener el `access_token`
4. Usar el token en peticiones protegidas si el proyecto sigue ampliándose con rutas autenticadas

## 📡 Endpoints principales

### Usuarios

- `POST /users` Crear usuario
- `POST /login` Iniciar sesión
- `GET /users` Obtener usuarios
- `GET /users/{user_id}` Obtener usuario por ID

### Categorías

- `POST /categories` Crear categoría
- `GET /categories/` Obtener todas las categorías
- `GET /categories/{category_id}` Obtener una categoría por ID
- `PATCH /categories/{category_id}` Actualizar categoría
- `DELETE /categories/{category_id}` Eliminar categoría
- `GET /categories/{category_id}/products` Obtener productos de una categoría

### Productos

- `POST /products` Crear producto
- `GET /products` Obtener productos con filtros
- `GET /products/{product_id}` Obtener producto por ID
- `PATCH /products/{product_id}` Actualizar producto
- `DELETE /products/{product_id}` Eliminar producto
- `GET /products/low-stock` Obtener productos con stock bajo

## 🗂️ Modelos principales

### User

- `id`
- `email`
- `password`

### Category

- `id`
- `name`

### Product

- `id`
- `name`
- `price`
- `stock`
- `category_id`
- `min_stock`
- `is_active`

## 📌 Estado del proyecto

El proyecto ya cuenta con una base funcional para la gestión de inventario, incluyendo autenticación, usuarios, categorías y productos. Aun así, todavía puede crecer con nuevas validaciones, protección de rutas, mejores respuestas de error y más funcionalidades orientadas a una tienda real.

## 👨‍💻 Autor

Desarrollado por `amayaronald75-lgtm`.
