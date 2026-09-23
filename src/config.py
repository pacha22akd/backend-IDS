import os #me da acceso a las variables de entorno
from dotenv import load_dotenv #me permite cargar el archivo .env
from flask_sqlalchemy import SQLAlchemy

load_dotenv() #carga las variables de entorno definivas en el .env

# URL base de la API
BASE_URL = '/club_deportivo_api'

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME = os.getenv('DB_NAME', 'club_deportivo')

#URI que flask-sqlalchemy lee automaticamente
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Creo el objeto db vacio para que pueda utilizarse y asociarse con la bd
db = SQLAlchemy()

# Formato de fecha esperado por la API
FORMATO_FECHA = '%Y-%m-%d'