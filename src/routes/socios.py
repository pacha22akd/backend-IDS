from flask import Blueprint, request, jsonify
from src.services import socios as socios_ser

socios_bp = Blueprint('socios_bp', __name__)

@socios_bp.route('/socios', methods=['POST'])

def crear_socio():
    datos = request.get_json()
    respuesta, status_code = socios_ser.registrar_nuevo_socio(datos)
    return jsonify(respuesta), status_code

@socios_bp.route('/socios', methods=['GET'])

def obtener_socios():
    args = request.args
    respuesta, status_code = socios_ser.listar_socios(args)

    return jsonify(respuesta), status_code