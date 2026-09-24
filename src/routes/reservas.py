from flask import Blueprint, request, jsonify
from src.services import reservas as reservas_service

reservas_bp = Blueprint('reservas', __name__)
@reservas_bp.route('/reservas', methods=['POST'])



def crear_reserva():

    #agarro los datos y los guardo como diccionario en datos
    datos = request.get_json()

    respuesta, estado = reservas_service.crear_reserva(datos)

    return jsonify(respuesta), estado