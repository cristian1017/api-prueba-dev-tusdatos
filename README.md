# Prueba Técnica Desarrollador Backend Python

## Descripción

Este proyecto tiene como objetivo extraer información de la página web [Consulta de Procesos Judiciales](https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros) mediante técnicas de web scraping y exponer dicha información a través de una API REST.

## Librerias

- Flask
- PyJWT
- Python-dotenv
- Requests
- Selenium
- Webdriver-manager
- Pytest

## Estructura del Proyecto

Este proyecto sigue una arquitectura hexagonal, la cual organiza el código en diferentes capas o módulos para mejorar la mantenibilidad y escalabilidad del software. La estructura de carpetas es la siguiente:

```
├── app/
│ ├── application/
│ │ └── services/
│ ├── distribution/
│ │ └── web/
│ │   └── server/
│ │     ├── routes/
│ │     ├── main.py
│ │     └── middleware.py
│ ├── domain/
│ ├── infrastructure/
│ │ ├── driver/
│ │ └── repositories/
│ │   ├── data_repository.py
│ │   └── data.json
│ ├── util/
│ ├── config.py
│ └── __init__.py
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

### Explicación de las carpetas principales

- **tests/**: Contiene todos los tests del proyecto, organizados por funcionalidades.
- **app/**: Carpeta principal de la aplicación que contiene diferentes submódulos siguiendo la arquitectura hexagonal.
  - **application/services/**: Contiene la lógica de negocio de la aplicación, incluyendo los servicios. Ejemplo, el servicio de Scrapping
  - **distribution/web/server/**: Contiene los archivos relacionados con la exposición de la aplicación a través de una API web. Incluye:
    - **main.py**: Punto de entrada principal del servidor.
    - **middleware.py**: Middleware para validar autenticación y autorizacion
    - **routes/**: Definición de las rutas de la API.
  - **infrastructure/**: Implementaciones concretas de las interfaces definidas en el dominio, divididas en:
    - **driver/**: Código que inicializa las opciones de instancia de Selenium Driver.
    - **repositories/**: Implementaciones de los repositorios para el acceso a datos.
  - **util/**: Utilidades y helpers que son utilizados en toda la aplicación.
  - **config.py**: Configuraciones generales de la aplicación.
  - **\_ \_ _init_ \_ \_ .py**: Inicialización del módulo `app`.

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip
- Virtualenv

### Pasos para la instalación

1. Clona el repositorio:

```sh
git clone https://github.com/cristian1017/api-prueba-dev-tusdatos.git api-test-tusdatos
cd api-test-tusdatos
```

2. Crea un entorno virtual:

```sh
python -m venv venv # ó virtualenv venv
```

3. Acceder al entorno virtual:

```sh
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

4. Instala las dependencias:

```sh
pip install -r requirements.txt
```

### Configuración

Este proyecto utiliza variables de entorno para la configuración, pero también proporciona valores por defecto para la mayoría de los parámetros. Puedes crear un archivo `.env` en la raíz del proyecto para sobrescribir los valores por defecto si es necesario.

El archivo `config.py` espera las siguientes variables en el archivo `.env`:

### Variables de Entorno

- `SECRET_KEY`: Clave secreta para JWT
- `AUTH_USERNAME`: Nombre de usuario para la autenticación.
- `AUTH_PASSWORD`: Contraseña para la autenticación.

Puedes crear un archivo .env en la raíz del proyecto y agregar estas variables si deseas cambiarlas:

```
SECRET_KEY=tu_clave_secreta
AUTH_USERNAME=tu_usuario
AUTH_PASSWORD=tu_contraseña
```

### Otras Configuraciones

- `is_get_activity_for_actuaciones_judiciales`: Esta variable controla si se deben obtener las actividades detalladas para las actuaciones judiciales durante el proceso de scraping. Valor por defecto: False, lo que significa que por defecto no se obtendrán detalles de las actuaciones judiciales.
- `is_view_chrome_headless`: Esta variable determina si el navegador Chrome se ejecutará en modo headless durante el scraping. El modo headless permite ejecutar Chrome sin una interfaz gráfica, lo cual es útil para entornos de servidor o para mejorar el rendimiento. Valor por defecto: True, lo que significa que Chrome se ejecutará en modo headless. Si quieres revisar el proceso y dar seguimiento al scraping, cambiarlo a `False`

## Uso

### Ejecutar la Aplicación

Inicia el servidor de Flask:

```sh
flask run
```

Puedes usar herramientas para realizar peticiones HTTP como postman y probar los Enpoints.

### Endpoints API REST

Los endpoints disponibles son:

- `POST /api/login`: Autenticación de usuario, que se explica en `Autenticación y Autorización`
- `GET /api/scraper`: Scraping, que se explica en `Web Scraping`
- `GET /api/data/<id>`: Obtiene la información de dicho identificador.
- `GET /api/data`: Obtiene lista de ID, que estan en el archivo data.json
- `GET /api/data/<id>`: Obtiene la información de dicho identificador.

### Autenticación y Autorización

1. Enviar una solicitud `POST` a `/api/login` con las credenciales. Puedes usar una herramienta como Postman para realizar esta prueba:

   - Configura una nueva solicitud en Postman.
   - Selecciona el método POST.
   - Introduce la URL http://localhost:5000/api/login , recuerda cambiar el puerto en dado caso que no sea `5000` cuando inicies la app.
   - En el cuerpo de la solicitud, selecciona `raw` y `JSON`, luego introduce las siguientes credenciales o las que se configuro en el archivo `.env`
   - Envía la solicitud. Si las credenciales son correctas, recibirás un token JWT en la respuesta.

```
{
  "username": "tusdatos",
  "password": "123456"
}
```

2. Usar el token en el encabezado Authorization para las solicitudes a los endpoints protegidos:
   - Configura una nueva solicitud en Postman para el endpoint que deseas probar.
   - En la sección de encabezados, añade un nuevo encabezado
     - Key: Authorization
     - Value: `Bearer <tu_token_jwt>`
   - Si manejas Postman, puedes tambien, dirigirte al tab Authorization, y seleccionar `Bearer Token` y agregar el `<tu_token_jwt>`
   - Envía la solicitud y podrás acceder a los endpoints protegidos.

### Web Scraping

Para ejecutar el scraping y almacenar los datos mediante la API una vez iniciada la api.

1. Realiza una solicitud GET a http://127.0.0.1:5000/api/scraper.
   - Configura una nueva solicitud en Postman.
   - Selecciona el método GET.
   - Envía la solicitud con su respectivo `Token` en los `Header`, que se explica en el paso anterior de `Autenticación y Autorización`
   - Envía la solicitud. Esto ejecutará el proceso de scraping y almacenará los datos obtenidos en el archivo `data.json` que se encuentra en la ruta de carpetas `app/infraestructure/repositories/data.json`

### Swagger

Para ingresar a la documentación de la API.

1. Realiza una solicitud GET a http://127.0.0.1:5000/swagger

### Consulta por ID

Obtiene la información de dicho identificador, con su respectiva data y contador de items, si tiene información de ofendidos y demandados, se mostrar el contador de cada uno.

1. Realiza una solicitud GET a http://127.0.0.1:5000/api/data/0968599020001, Envía la solicitud con su respectivo `Token` en los `Headers`

### Testing

Los tests están ubicados en `app/tests/`. Para ejecutarlos:

```sh
pytest
```

### Punto Opcional: Desarrollar una vista
Se desarrolló una vista adicional utilizando `React.JS` que permite ejecutar la petición a la fuente y una vez terminada, ver de forma estructurada la información de los procesos. Esta vista proporciona una interfaz amigable para visualizar los datos obtenidos de la API, mostrando detalles.

Para descargar el proyecto y ejecutar [Frontend Test tusdatos.co](https://github.com/cristian1017/front-dev-tusdatos)
