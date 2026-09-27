def validar_datos_cancha(datos):
    
    if 'id_deporte' in datos or 'deporte' in datos:
        return False, "No se puede modificar el deporte de una cancha existente"


    if 'precio' in datos and datos['precio'] <= 0:
        return False, "El precio debe ser mayor a 0"
        
    return True, ""