import logging
from flask import Flask
from src.config import db
from src.routes.deportes import deportes_bp
from src.routes.socios import socios_bp

# Configuración de los logs
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__)
app.json.sort_keys = False

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# Recuerda cambiar 'root', 'password' y 'nombre_db' por tus credenciales reales
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/nombre_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos con Flask
db.init_app(app)

# Registramos el blueprint de deportes. 
# Si antes usabas un BASE_URL como '/api', lo ponemos directamente aquí:
app.register_blueprint(deportes_bp, url_prefix='/api')
app.register_blueprint(socios_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)