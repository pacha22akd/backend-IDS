from flask import Blueprint, request, jsonify
from src.services import socios as socios_ser

socios_bp = Blueprint('socios_bp', __name__)

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

@socios_bp.route('/socios', methods=['POST'])

def crear_socio():
    datos = request.get_json()
    respuesta, status_code = socios_ser.registrar_nuevo_socio(datos)

    if status_code >= 400:
        return crear_respuesta_error(
            respuesta["error"],
            status_code
        )

    return respuesta, status_code

@socios_bp.route('/socios', methods=['GET'])

def obtener_socios():
    args = request.args
    respuesta, status_code = socios_ser.listar_socios(args)

    if status_code >= 400:
        return crear_respuesta_error(
            respuesta["error"],
            status_code
        )

    if status_code == 204:
        return "", 204

    return jsonify(respuesta), 200

#SOFIIII----------------

#PRE: Debe recibir un id del tipo entero.
#POST: 
# Si el método es "GET": Devuelve en formato json los datos del socio solicitado. Si no lo encuentra devuelve el error SOCIO_NO_ENCONTRADO.
@socios_bp.route("/socios/<int:id>", methods = ["GET", "PATCH"])
def socios_id(id):
    if request.method == "PATCH":
        try:
            if not request.is_json:
                return crear_errores("ERROR_VALIDACION", "El cuerpo de la solicitud es inválido", "El cuerpo de la solicitud debe ser JSON."), 400
            modificaciones = request.get_json(silent=True)

            if modificaciones is None: #Verificamos que sea un json válido.
                return crear_respuesta_error( "El cuerpo debe contener un JSON válido.", 400)
            resultado_modificacion = socios_ser.modificar_socio(id, modificaciones)

            if "error" in resultado_modificacion:
                if resultado_modificacion["error"] == "validacion":
                    return crear_respuesta_error(resultado_modificacion["descripcion"], 400)
                elif resultado_modificacion["error"] == "No encontrado":
                    return crear_respuesta_error(resultado_modificacion["descripcion"], 404)
                elif resultado_modificacion["error"] == "Email repetido":
                    return crear_respuesta_error(resultado_modificacion["descripcion"], 409)

            return "", 204

        except Exception:
                return crear_errores("ERROR_INTERNO", "Error interno del servidor", "Ocurrió un error al actualizar el socio."), 500

    try:
        socio_buscado = socios_ser.obtener_socio_por_id(id)

    except Exception:
        return crear_respuesta_error("Ocurrió un error al buscar el socio.", 500)

    if socio_buscado is None: 
        return crear_respuesta_error(f"No existe el socio con id {id}.", 404)

    return dict(socio_buscado), 200
