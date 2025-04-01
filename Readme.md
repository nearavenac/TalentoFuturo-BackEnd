# Sistema de Reporte

Proyecto para registrar y reportar medidas de avance de los PPDA por parte de los organismos sectoriales, con enfoque en el plan de Concón, Quintero y Puchuncaví.

## Requisitos
- Python (3.x)
- PostgreSQL

## Pasos para levantar el proyecto

### 1. Crear y activar el entorno virtual

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias
Asegúrate de tener el archivo requirements.txt actualizado y ejecuta:

```bash
pip install -r requirements.txt
```

### 3. Configurar las variables de entorno
Crea o actualiza el archivo .env en la raíz del proyecto con el siguiente contenido:

```ini
DB_USER=postgres
DB_PASSWORD=admin
DEBUG=True
```

### 4. Ejecutar migraciones
Genera y aplica las migraciones de la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Iniciar el servidor de desarrollo
Levanta el servidor con:

```bash
python manage.py runserver
```

Puedes levantar el servidor con https:

```bash
python -m uvicorn plan_prevencion.asgi:application \
    --reload \
    --ssl-keyfile=key.pem \
    --ssl-certfile=cert.pem \
    --host 127.0.0.1 \
    --port 8000
```