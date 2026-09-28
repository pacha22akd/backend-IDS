# CLUB DEPORTIVO - API

API REST desarrollada en Python y Flask para gestionar canchas, socios y reservas
de un club.

## Documentacion Swagger

Esta API la desarrollamos siguiendo al pie de la letra el contrato Swagger que se nos ha brindado.

-Para visalizarlo, puede pegar el contenido del archivo Swagger en (https://editor.swagger.io).

## Estructura del proyecto

```
club-deportivo-api/
├── app.py                          # Archivo que corre la API con Flask en el puerto 5000.            
├── requirements.txt                # Dependencias Python.
├── .env.example                    # Variables de entorno para configurar la base de datos.
├── src/
│   ├── config.py                   # Configuracion de la Base de datos.
│   ├── repositories/               # Ejecuta sentencias SQL para pedirle datos a la base de datos.
│   │   ├── canchas.py 
│   │   ├── deportes.py 
│   │   ├── reservas.py 
│   │   └── socios.py
│   ├── routes/                     # Endpoints REST de la API. 
│   │   ├── canchas.py 
│   │   ├── deportes.py 
│   │   ├── reservas.py 
│   │   └── socios.py
│   ├── services/                   # Contienen las reglas de negocio.
│   │   ├── canchas.py 
│   │   ├── deportes.py 
│   │   ├── reservas.py 
│   │   └── socios.py
│   └── validators/                 # Validan los datos que ingresa el usuario.
│   │   ├── canchas.py  
│   │   ├── reservas.py 
│   │   └── socios.py
├── db/
│   └── init_db.sql                 # Script SQL que levanta las tablas de la base de datos.
└── docs/
    └── swagger.yaml                # Contrato a seguir.
```

## Requisitos previos

Python 3.10+ y tener instalado localmente MySQL 8.0.46.

## Configuracion

### 1 - Variables de entorno:
copiar `.env.example` a `.env`:

```bash
cp .env.example .env
```

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=club_deportivo
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

Modifica las variables en base a tu configuracion SQL.

### 2 - Base de datos MySQL

1. Crear la base de datos y correr el init_db.sql:

```powershell
# Windows PowerShell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS club_deportivo;"
Get-Content db\init_db.sql | mysql -u root -p club_deportivo
```

```bash
# Linux / macOS / WSL
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS club_deportivo;"
mysql -u root -p club_deportivo < db/init_db.sql
```

2. Verificar que las tablas esten cargadas en la base de datos:

```powershell
# Windows PowerShell
mysql -u root -p -e "USE club_deportivo; SHOW TABLES;"
```

```bash
# Linux / macOS / WSL
mysql -u root -p -e "USER club_deportivo; SHOW TABLES;"
```

### 3 - Entorno virtual con virtualenv

```bash
# Windows
setup_virtualenv.bat

# Linux / macOS
chmod +x setup_virtualenv.sh
./setup_virtualenv.sh
```

## ENDPOINTS

Todos los Endpoints estan bajo el prefijo '/club_deportivo_api'. 
Las respuestas son en formato JSON.

### `GET /deportes`

Lista todos los deportes.

Respuesta `200 OK`:

```json
[
    {
        "nombre": "Futbol"
    },
    {
        "nombre": "Tenis"
    },
    {
        "nombre": "Padel"
    }
]
```

Si no hay deportes cargados, devuelve `204 No Content`.

### `GET /reservas`

Respuesta `200 OK`:

```json
{
    "reservas": [
        {
            "id": 1,
            "id_cancha": 1,
            "id_socio": 1,
            "fecha_hora_inicio": "Thu, 15 Oct 2026 18:00:00 GMT",
            "fecha_hora_fin": "Thu, 15 Oct 2026 20:00:00 GMT",
            "estado": "confirmada",
            "precio_hora": 1000000,
            "precio_total": 2000000
        }
    ]
}
```
Si no hay reservas cargadas, devuelve `204 No Content`.

### `GET /socios/id`

Respuesta `200 OK`:

```json
{
    "id": 1,
    "nombre": "Ana G??mez",
    "email": "ana.gomez@example.com",
    "activo": 1
}
```

Si no hay socios cargados, devuelve `204 No Content`.

