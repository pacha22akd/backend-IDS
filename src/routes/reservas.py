from flask import Blueprint, request, jsonify
from src.services import reservas as reservas_service
from src.routes.socios import crear_respuesta_error, crear_errores

reservas_bp = Blueprint('reservas', __name__)
def crear_errores(codigo: str, mensaje: str, descripcion: str) -> dict:
    return {
        "errors": [ 
            {
                "code": codigo,
                "message": mensaje,
                "level": "error",
                "description": descripcion
            } 
        ]
    }

def crear_respuesta_error(descripcion, status_code):

    if status_code == 400:
        return crear_errores(
            "ERROR_VALIDACION",
            "El cuerpo de la solicitud es inválido",
            descripcion
        ), 400

    if status_code == 404:
        return crear_errores(
            "SOCIO_NO_ENCONTRADO",
            "Recurso no encontrado",
            descripcion
        ), 404

    if status_code == 409:
        return crear_errores(
            "EMAIL_EN_USO",
            "Conflicto de negocio",
            descripcion
        ), 409

    return crear_errores(
        "ERROR_INTERNO",
        "Error interno del servidor",
        descripcion
    ), 500

@reservas_bp.route('/reservas', methods=['GET'])

def get_reservas():

    id_cancha = request.args.get("id_cancha")

    id_socio = request.args.get("id_socio")

    estado = request.args.get("estado")

    fecha_desde = request.args.get("fecha_desde")

    fecha_hasta = request.args.get("fecha_hasta")

    limit = request.args.get("_limit", default=10, type=int)

    offset = request.args.get("_offset", default=0, type=int)

    try:
        reservas = reservas_service.listar_reservas(id_cancha, id_socio, estado, fecha_desde, fecha_hasta, limit, offset)

        if reservas is not None:

            return jsonify({"reservas": reservas}), 200

        else:

            return "", 204 

    except ValueError as error:

        return crear_respuesta_error(error, 400)
    
    except Exception:
    
        return jsonify({"error": str()}), 500

@reservas_bp.route('/reservas', methods=['POST'])



def crear_reserva():
    try:
        #agarro los datos y los guardo como diccionario en datos
        datos = request.get_json()

        respuesta, nueva_reserva = reservas_service.crear_reserva(datos)

        return jsonify(respuesta), nueva_reserva,

    except Exception:
         return crear_respuesta_error("Error interno del servidor", 500)
