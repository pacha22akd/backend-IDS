import re

#SOFIII---
def validacion_nombre(nombre):
    return (type(nombre) == str) and (nombre.strip() != "")

def validacion_activo(actividad):
    return type(actividad) == bool

#EUGEE------
def validacion_email(email):
    #Valido si el email es un String
    if not isinstance(email, str):
        return False

    email_limpio = email.strip().lower()

    VALIDACION_EMAIL = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(VALIDACION_EMAIL, email_limpio))

def validacion_socio(datos):
    if not datos:
        return "No hay datos ingresados."
    
    nombre = datos.get('nombre')
    if not nombre or not validacion_nombre(nombre):
        return "Debe ingresar un nombre obligatoriamente, no puede estar vacío."
    
    email = datos.get('email')
    if not email or not isinstance(email,str) or not email.strip():
        return "Debe ingresar un email obligatoriamente, no puede estar vacío."
 
    es_valido = validacion_email(email)
    
    if not es_valido:
        return "El formato del correo electrónico es inválido."   

    return None

#SOFIII-----

def validar_modificaciones_socio(modificaciones):
    if type(modificaciones) != dict:
        return {
            "error": "validacion",
            "descripcion": "El cuerpo de la solicitud debe ser un JSON."
            }

    if not modificaciones:
        return {
            "error": "validacion",
            "descripcion": "El cuerpo de la solicitud no puede estar vacío."
        }

    campos_permitidos = {"nombre", "email", "activo"}

    for campo in modificaciones:
        if campo not in campos_permitidos:
            return {
                "error": "validacion",
                "descripcion": f"El campo '{campo}' no está permitido."
            }
    
    if "nombre" in modificaciones:
        es_valido_nombre = validacion_nombre(modificaciones["nombre"]) #el nombre no debería de estar vacío
        if not es_valido_nombre:
            return {
                "error": "validacion", 
                "descripcion": "El nombre no puede estar vacío."
            }
        
    if "email" in modificaciones:
        es_valido_email = validacion_email(modificaciones["email"])
        if not es_valido_email: 
            return {
                "error": "validacion", 
                "descripcion": "El formato del correo electrónico es inválido."
                }

    if "activo" in modificaciones:
        es_valido_actividad = validacion_activo(modificaciones["activo"]) #activo debe ser bool
        if not es_valido_actividad:
            return {
                "error": "validacion", 
                "descripcion": "El dato de la actividad debe ser un bool válido."
            }

    return None
