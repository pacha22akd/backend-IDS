from flask import Blueprint, request, jsonify

from src.services.canchas import (
    obtener_todas_canchas,
    crear_cancha,
    eliminar_cancha
)
from src.services import canchas as canchas_service

from src.services.canchas import (
    obtener_cancha, 
    actualizar_cancha_parcial, 
    consultar_disponibles
)

canchas_bp = Blueprint("canchas_bp", __name__)

@canchas_bp.route('', methods=['GET'])

def crear_errores(codigo, mensaje, descripcion):
    return {
        "errors": [
            {
                "code": codigo,
                "message": mensaje,
                "level": "error",
                "description": descripcion,
            }
        ]
    }


def crear_respuesta_error(descripcion, status_code):
    if status_code == 400:
        return jsonify(crear_errores("ERROR_VALIDACION", "El cuerpo de la solicitud es inválido", descripcion)), 400
    if status_code == 404:
        return jsonify(crear_errores("CANCHA_NO_ENCONTRADA", "Recurso no encontrado", descripcion)), 404
    if status_code == 409:
        return jsonify(crear_errores("CANCHA_CON_RESERVAS", "Conflicto de negocio", descripcion)), 409
    return jsonify(crear_errores("ERROR_INTERNO", "Error interno del servidor", descripcion)), 500


@canchas_bp.route("/canchas", methods=["GET"])
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


@canchas_bp.route("/canchas/disponibles", methods=["GET"])
def listar_canchas_disponibles():
    try:
        return jsonify(canchas_service.listar_canchas_disponibles(request.args, request.base_url)), 200
    except ValueError as error:
        return crear_respuesta_error(str(error), 400)
    except Exception:
        return crear_respuesta_error("Ocurrió un error al consultar la disponibilidad.", 500)


@canchas_bp.route("/canchas/<int:cancha_id>", methods=["GET"])
def obtener_cancha(cancha_id):
    try:
        cancha = canchas_service.obtener_cancha_por_id(cancha_id)
        if cancha is None:
            return crear_respuesta_error("No existe la cancha solicitada.", 404)
        return jsonify(cancha), 200
    except ValueError as error:
        return crear_respuesta_error(str(error), 400)
    except Exception:
        return crear_respuesta_error("Ocurrió un error al buscar la cancha.", 500)


@canchas_bp.route("/canchas", methods=["POST"])
def crear_cancha():
    try:
        return jsonify(canchas_service.crear_cancha(request.get_json(silent=True))), 201
    except ValueError as error:
        return crear_respuesta_error(str(error), 400)
    except Exception:
        return crear_respuesta_error("Ocurrió un error al crear la cancha.", 500)


@canchas_bp.route("/canchas/<int:cancha_id>", methods=["PATCH"])
def actualizar_cancha(cancha_id):
    try:
        cancha = canchas_service.actualizar_cancha(cancha_id, request.get_json(silent=True))
        if cancha is None:
            return crear_respuesta_error("No existe la cancha solicitada.", 404)
        return "", 204
    except ValueError as error:
        return crear_respuesta_error(str(error), 400)
    except Exception:
        return crear_respuesta_error("Ocurrió un error al actualizar la cancha.", 500)


@canchas_bp.route("/canchas/<int:cancha_id>", methods=["DELETE"])
def eliminar_cancha(cancha_id):
    try:
        resultado = canchas_service.eliminar_cancha(cancha_id)
        if resultado == "no_encontrada":
            return crear_respuesta_error("No existe la cancha solicitada.", 404)
        if resultado == "con_reservas":
            return crear_respuesta_error("La cancha tiene reservas asociadas y no puede eliminarse.", 409)
        return "", 204
    except ValueError as error:
        return crear_respuesta_error(str(error), 400)
    except Exception:
        return crear_respuesta_error("Ocurrió un error al eliminar la cancha.", 500)
