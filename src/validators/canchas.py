def validacion_nombre(nombre):
    return isinstance(nombre, str) and bool(nombre.strip())


def validacion_entero_positivo(valor):
    return type(valor) is int and valor > 0


def validacion_booleano(valor):
    return type(valor) is bool


def validar_cancha(datos, es_alta):
    if not isinstance(datos, dict):
        return "El cuerpo debe contener un objeto JSON válido."
    if not datos:
        return "El cuerpo de la solicitud no puede estar vacío."
    permitidos = {"nombre", "precio_hora", "techada", "activa"}
    if es_alta:
        permitidos.add("id_deporte")
        faltantes = {"nombre", "id_deporte", "precio_hora"} - set(datos)
        if faltantes:
            return f"Falta el campo obligatorio '{sorted(faltantes)[0]}'."
    desconocidos = set(datos) - permitidos
    if desconocidos:
        return f"El campo '{sorted(desconocidos)[0]}' no está permitido."
    if "nombre" in datos and not validacion_nombre(datos["nombre"]):
        return "El nombre debe ser un texto no vacío."
    if "id_deporte" in datos and not validacion_entero_positivo(datos["id_deporte"]):
        return "id_deporte debe ser un entero mayor o igual a 1."
    if "precio_hora" in datos and not validacion_entero_positivo(datos["precio_hora"]):
        return "precio_hora debe ser un entero mayor o igual a 1."
    for campo in ("techada", "activa"):
        if campo in datos and not validacion_booleano(datos[campo]):
            return f"El campo {campo} debe ser booleano."
    return None
