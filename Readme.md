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

### 6. Explicación de EndPoints

Para ver la documentación y realizar pruebas puede ingresar a:

[Documentación Swagger](http://127.0.0.1:8000/api/docs/)

## Explicación de Front 

<p align='center'>Se recrearon los endpoints anteriores con renderización de HTML para mejorar su comprención y aplicabilidad. A continuación se explicarán en terminos generales que realiza cada ruta.

Al ingresas al dominio ([http://127.0.0.1:8000/](http://127.0.0.1:8000/)), se renderizara por defecto  `home.html`. En este template tenemos varias acciones posibles. </p>

1. Registrarnos para poder acceder a visualizar y verificar diferentes acciones dentro del **panel de usuarios** (estados de las medidas).
2. Iniciar sesión como usuario (los usuarios registrados unicamente tendras este acceso).
3. Iniciar sesión como administrador.
    
<p align='center'>Una vez se inicie sesión como **usuario**, estará disponible el panel en la parte superior izquierda, en donde podemos evaluar y visualizar el estado de las medidas. Hay que recalcar que para entrar como usuario un administrador debe permitir al usuario.</p>

### Panel de administrador

<p align='center'>En caso de que iniciemos sesión como administrador, tendremos varias opción para elegir.</p>

1. **Pestaña de Usuario**: En la pantalla principal, notaremos que podemos administrar los usuarios que se quieran registrar. Tendremos acciones de aprobar a un nuevo usuario como de desactivar su cuenta.
2. **Pestaña de Reportes**: En este apartado se tendra un registro del estado general de una medida, añadiendo información de los responsables, estados y acciones a tomar para cada uno de los planes.
3. **Pestaña de Mantenedores**: En esta pestaña se pueden administrar los organismos publicos existentes, las comunas, los tipos de medida y las medidas (Agregar, editar y eliminar).
    