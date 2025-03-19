Proyecto creado en sistema operativo windows
Proyecto: Sistema de Reporte
Objetivo: Registrar y reportar medidas de avance de los PPDA por parte de los organismos
sectoriales, con enfoque en el plan de Concón, Quintero y Puchuncaví
lenguaje: Python
framework: Django
base de datos: PostgreSQL
editor de codigo: Visual Studio Code
pruebas API REST con Postman


# crear y activar entorno vistual
python -m venv venv

# instalar django
pip install django

# crear proyecto
django-admin startproject plan_prevencion

# crear app
django-admin startapp proyecto_prevencion

# ejecutar servidor
python manage.py runserver

# verificar cambios  en el model aplicados a la base de datos
python manage.py makemigrations

# ejecutar migraciones reflejadas en la base de datos
python manage.py migrate

# configurar el settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'proyecto_prevencion',
    'rest_framework',
    'drf_spectacular',
]

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ppda',
        'USER': 'xxxxxx', colocar las credenciales de postgres
        'PASSWORD': 'xxxxxx', colocar las credenciales de postgres
        'HOST': 'localhost',
        'PORT': '5432',
    }
}