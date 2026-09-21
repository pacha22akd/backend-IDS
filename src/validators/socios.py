import re

def validacion_email(email):
    #Valido si el email es un String
    if not isinstance(email, str):
        return False
    VALIDACION_EMAIL = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(VALIDACION_EMAIL, email))

def validacion_socio(datos):
    if not datos:
        return "No hay datos ingresados."
    
    nombre = datos.get('nombre')
    if not nombre or not isinstance(nombre,str) or not nombre.strip():
        return "Debe ingresar un nombre obligatoriamente, no puede estar vacío."
    
    email = datos.get('email')
    if not email or not isinstance(email,str) or not email.strip():
        return "Debe ingresar un email obligatoriamente, no puede estar vacío."

    email_limpio = email.strip().lower()
    es_valido = validacion_email(email_limpio)
    
    if not es_valido:
        return "El formato del correo electrónico es inválido."   

    return None

