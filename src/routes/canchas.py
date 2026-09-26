from flask import Blueprint, request, jsonify
from src.services.canchas import (
    obtener_todas_canchas,
    obtener_cancha_por_id,
    crear_cancha,
    actualizar_cancha,
    eliminar_cancha
)

canchas_bp = Blueprint('canchas', __name__, url_prefix='/canchas')

@canchas_bp.route('/canchas', methods=['GET'])
def listar_canchas():
    canchas = obtener_todas_canchas()
    return jsonify([c.to_dict() for c in canchas]), 200

@canchas_bp.route('/canchas/<int:cancha_id>', methods=['GET'])
def ver_cancha(cancha_id):
    cancha = obtener_cancha_por_id(cancha_id)
    if not cancha:
        return jsonify({"mensaje": "Cancha no encontrada"}), 404
    return cancha, 200

@canchas_bp.route('/canchas', methods=['POST'])
def nueva_cancha():
    datos = request.get_json()
    cancha = crear_cancha(datos)
    return jsonify(cancha.to_dict()), 201

@canchas_bp.route('/canchas/<int:cancha_id>', methods=['PUT'])
def editar_cancha(cancha_id):
    datos = request.get_json()
    cancha = actualizar_cancha(cancha_id, datos)
    if not cancha:
        return jsonify({"mensaje": "Cancha no encontrada"}), 404
    return jsonify(cancha.to_dict()), 200

@canchas_bp.route('/canchas/<int:cancha_id>', methods=['DELETE'])
def borrar_cancha(cancha_id):
    cancha = eliminar_cancha(cancha_id)
    if not cancha:
        return jsonify({"mensaje": "Cancha no encontrada"}), 404
    return jsonify({"mensaje": "Cancha eliminada"}), 200