# Simple CRUD con Django 5.2 LTS

CRUD de local de comida, carga de imágenes y SQLite.

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

### Windows PowerShell

```powershell
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
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre http://127.0.0.1:8000/ para iniciar sesión y http://127.0.0.1:8000/admin/ para administrar categorías y productos.

## Variables de entorno opcionales

- `DJANGO_SECRET_KEY`: clave secreta del proyecto.
- `DJANGO_DEBUG`: `True` o `False`.
- `DJANGO_ALLOWED_HOSTS`: hosts separados por coma.

Los valores predeterminados están pensados únicamente para desarrollo local.
