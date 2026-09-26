from flask import Blueprint, jsonify
from src.services.deportes import listar_deportes
import logging

# Creamos el blueprint para deportes
deportes_bp = Blueprint('deportes_bp', __name__)
logger = logging.getLogger(__name__)

@deportes_bp.route('/deportes', methods=['GET'])
def get_deportes():
    try:
        deportes = listar_deportes()
        if not deportes:
            return '', 204
        return jsonify(deportes), 200
    except Exception as e:
        logger.error(f"Error al listar deportes: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500