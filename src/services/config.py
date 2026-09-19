import os #me da acceso a las variables de entorno
from dotenv import load_dotenv #me permite cargar el archivo .env

load_dotenv() #carga las variables de entorno definivas en el .env

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME = os.getenv('DB_NAME', 'club_deportivo')

#URI que flask-sqlalchemy lee automaticamente
SQLALCHEMY_DATABASE_URI = (
    f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}'
    f'@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

#DEFINIR EL RESTO DE VARIABLES DE ENTORNO ACA