from flask import Blueprint, request, jsonify

from src.services.canchas import (
    obtener_todas_canchas,
    crear_cancha,
    eliminar_cancha
)

from src.services.canchas import (
    obtener_cancha, 
    actualizar_cancha_parcial, 
    consultar_disponibles
)

canchas_bp = Blueprint('canchas', __name__, url_prefix='/canchas')

@canchas_bp.route('', methods=['GET'])
def listar_canchas():
    canchas = obtener_todas_canchas()
    return jsonify([c.to_dict() for c in canchas]), 200

@canchas_bp.route('', methods=['POST'])
def nueva_cancha():
    datos = request.get_json()
    cancha = crear_cancha(datos)
    return jsonify(cancha.to_dict()), 201

@canchas_bp.route('/disponibles', methods=['GET'])
def disponibles():
    return consultar_disponibles(request.args)

@canchas_bp.route('/<int:cancha_id>', methods=['GET'])
def ver_cancha(cancha_id):
    return obtener_cancha(cancha_id)

@canchas_bp.route('/<int:cancha_id>', methods=['PATCH'])
def editar_cancha(cancha_id):
    datos = request.get_json()
    return actualizar_cancha_parcial(cancha_id, datos)

@canchas_bp.route('/<int:cancha_id>', methods=['DELETE'])
def borrar_cancha(cancha_id):
    cancha = eliminar_cancha(cancha_id)
    if not cancha:
        return jsonify({"mensaje": "Cancha no encontrada"}), 404
    return jsonify({"mensaje": "Cancha eliminada"}), 200