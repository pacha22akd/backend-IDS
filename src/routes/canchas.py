from flask import Blueprint, jsonify, request

from src.services import canchas as canchas_service


canchas_bp = Blueprint("canchas_bp", __name__)


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
    try:
        return jsonify(canchas_service.listar_canchas(request.args, request.base_url)), 200
    except ValueError as error:
        return crear_respuesta_error(str(error), 400)
    except Exception:
        return crear_respuesta_error("Ocurrió un error al listar las canchas.", 500)


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
