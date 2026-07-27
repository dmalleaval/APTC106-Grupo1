# APTC106-Grupo1
Repositorio correspondiente a sección APTC106 Taller de desarrollo web y movil Grupo 1

## Integrantes

- Isabel Vera
- Gabriel Vera
- Diego Mallea

## Descripción del proyecto

CRUD de local de comida hecho con Django 5.2, con carga de imágenes y base de datos SQLite. El código fuente está en la carpeta [codigo/](codigo/).

## Requisitos

- Python 3.10 o superior
- pip

## Instalación y ejecución

Todos los comandos se ejecutan dentro de la carpeta `codigo/`.

### Windows (PowerShell)

```powershell
cd codigo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Linux o macOS

```bash
cd codigo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`createsuperuser` pedirá username, email (opcional) y contraseña, para poder ingresar al panel de administración.

Con el servidor corriendo, abrir:

- Sitio: http://127.0.0.1:8000/
- Panel de administración: http://127.0.0.1:8000/admin/

### Siguientes veces (sin repetir toda la instalación)

```powershell
cd codigo
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

## Variables de entorno opcionales

- `DJANGO_SECRET_KEY`: clave secreta del proyecto.
- `DJANGO_DEBUG`: `True` o `False`.
- `DJANGO_ALLOWED_HOSTS`: hosts separados por coma.

Los valores predeterminados están pensados únicamente para desarrollo local.

## Notas

- Si se modifica algún modelo, generar y aplicar las migraciones antes de levantar el servidor:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- La base de datos SQLite (`codigo/db.sqlite3`) ya viene con datos de ejemplo cargados por el equipo.
