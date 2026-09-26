import logging
from flask import Flask
from src.config import (db, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, BASE_URL)
from src.routes.deportes import deportes_bp
from src.routes.socios import socios_bp
from src.routes.reservas import reservas_bp

# Configuración de los logs
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__)
app.json.sort_keys = False

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# Recuerda cambiar 'root', 'password' y 'nombre_db' por tus credenciales reales
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Inicializamos la base de datos con Flask
db.init_app(app)

# Registramos el blueprint de deportes. 
# Si antes usabas un BASE_URL como '/api', lo ponemos directamente aquí:
app.register_blueprint(deportes_bp, url_prefix=BASE_URL)
app.register_blueprint(socios_bp, url_prefix=BASE_URL)
app.register_blueprint(reservas_bp, url_prefix=BASE_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5000)