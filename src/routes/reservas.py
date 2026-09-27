from flask import Blueprint, request, jsonify
from src.services import reservas as reservas_service
from src.routes.socios import crear_respuesta_error

reservas_bp = Blueprint('reservas', __name__)
@reservas_bp.route('/reservas', methods=['POST'])



def crear_reserva():
    try:
        datos = request.get_json()
        respuesta, status_code = reservas_service.crear_reserva(datos)
        if status_code == 201:
            return "", 201

        return jsonify(respuesta), status_code,

    except Exception as e:
        print("----------------------------------------")
        print("ERROR REAL DETECTADO:", repr(e))  # Imprime la falla en la terminal de Flask
        print("----------------------------------------")
        
        return crear_respuesta_error("Error interno del servidor", 500)

    