from flask import Blueprint, request, jsonify
from src.services import reservas as reservas_service
from src.routes.socios import crear_respuesta_error, crear_errores

reservas_bp = Blueprint('reservas', __name__)
@reservas_bp.route('/reservas', methods=['POST'])



def crear_reserva():
    try:
        #agarro los datos y los guardo como diccionario en datos
        datos = request.get_json()

        respuesta, nueva_reserva = reservas_service.crear_reserva(datos)

        return jsonify(respuesta), nueva_reserva,

    except Exception:
         return crear_respuesta_error("Error interno del servidor", 500)