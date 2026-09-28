def validar_estado_reserva(datos):
    if not isinstance(datos, dict):
        return {
            "error": "validacion",
            "descripcion": "El cuerpo de la solicitud debe ser un objeto JSON."
        }

    if not datos:
        return {
            "error": "validacion",
            "descripcion": "El cuerpo de la solicitud no puede estar vacío."
        }

    campos_permitidos = {"estado"}

    for campo in datos:
        if campo not in campos_permitidos:
            return {
                "error": "validacion",
                "descripcion": f"El campo '{campo}' no está permitido."
            }

    estado = datos.get('estado')
    estados_validos = {"confirmada", "cancelada", "finalizada"}

    if not estado or estado not in estados_validos:
        return {
            "error": "validacion",
            "descripcion": "El estado ingresado debe ser 'confirmada', 'cancelada' o 'finalizada'."
        }

    return None