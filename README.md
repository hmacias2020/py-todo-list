# TODO List App

Aplicación completa para gestión de tareas (TODO list) con un backend REST API construido con FastAPI y SQLAlchemy, y un frontend estético en HTML/CSS/JavaScript. Incluye autenticación de usuarios mediante JWT (JSON Web Token).

Los datos se almacenan en una base de datos SQLite en memoria, por lo que se reinician al detener el servidor.

## Requisitos

- Python 3.12+

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python -m uvicorn app.main:app --reload
```

El servidor se levanta en `http://localhost:8000`.

Para configurar la clave secreta de JWT, establece la variable de entorno `SECRET_KEY`:

```bash
SECRET_KEY=mi-clave-secreta python -m uvicorn app.main:app --reload
```

## Frontend

Al acceder a `http://localhost:8000` se sirve la interfaz web con las siguientes características:

- ✅ Diseño moderno con gradientes y animaciones suaves
- ✅ Crear, completar y eliminar tareas
- ✅ Filtrar tareas por estado (todas, pendientes, completadas)
- ✅ Estadísticas en tiempo real
- ✅ Diseño responsivo para móviles y escritorio
- ✅ Descripción opcional para cada tarea
- ✅ Pantalla de login y registro de usuarios
- ✅ Autenticación con JWT para proteger las operaciones

## Autenticación

La aplicación utiliza JWT para proteger las rutas de la API. El flujo de autenticación es:

1. El usuario se registra en `/auth/register` con un nombre de usuario y contraseña.
2. El usuario inicia sesión en `/auth/login` y recibe un token JWT.
3. El token se almacena en `localStorage` en el navegador.
4. Todas las peticiones a `/todos/` incluyen el token en el header `Authorization: Bearer <TOKEN>`.
5. Si el token es inválido o ha expirado, el usuario es redirigido a la pantalla de login.

**Usuario por defecto:** Al iniciar la aplicación se crea automáticamente el usuario `Haydee` con contraseña `Summer`.

## Endpoints

### Autenticación

| Método | Ruta              | Descripción                              |
|--------|-------------------|------------------------------------------|
| `POST` | `/auth/register`  | Registrar un nuevo usuario               |
| `POST` | `/auth/login`     | Iniciar sesión y obtener token JWT       |

### Tareas (requieren autenticación)

| Método   | Ruta            | Descripción                                      |
|----------|-----------------|--------------------------------------------------|
| `POST`   | `/todos/`       | Crear un nuevo todo                              |
| `GET`    | `/todos/`       | Listar todos (filtro opcional `?completed=true`)  |
| `GET`    | `/todos/{id}`   | Obtener un todo por ID                           |
| `PUT`    | `/todos/{id}`   | Actualizar un todo                               |
| `DELETE` | `/todos/{id}`   | Eliminar un todo                                 |

## Ejemplos

Registrar un usuario:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "miusuario", "password": "mipassword"}'
```

Iniciar sesión:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "miusuario", "password": "mipassword"}'
```

Crear un todo (con token):

```bash
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"title": "Comprar leche", "description": "En el supermercado"}'
```

Listar todos (con token):

```bash
curl http://localhost:8000/todos/ \
  -H "Authorization: Bearer <TOKEN>"
```

Actualizar un todo (con token):

```bash
curl -X PUT http://localhost:8000/todos/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"completed": true}'
```

Eliminar un todo (con token):

```bash
curl -X DELETE http://localhost:8000/todos/1 \
  -H "Authorization: Bearer <TOKEN>"
```
