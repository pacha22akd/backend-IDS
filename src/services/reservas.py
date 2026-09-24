from datetime import datetime
from src.repositories import socios as socios_repo
from src.repositories import canchas as canchas_repo
from src.repositories import reservas as reservas_repo

def crear_reserva(datos):

    id_socio = datos.get('id_socio')
    id_cancha = datos.get('id_cancha')
    inicio = datos.get('inicio')
    fin = datos.get('fin')
    socio = socios_repo.buscar_socio_por_id(id_socio)
    cancha = canchas_repo.buscar_cancha_por_id(id_cancha)
    hora_inicio = datetime.fromisoformat(inicio)
    hora_fin = datetime.fromisoformat(fin)
    
   

    if not all([id_socio, id_cancha, inicio, fin]):
            return {"error": "Faltan datos requeridos"}, 400
    
    if socio is None:
        return {"error": "Socio no encontrado"}, 404

    actividad = socio.get('activo')

    if not actividad:
        return {"error": "El socio no está activo"}, 400

    if hora_inicio < datetime.now():
        return {"error": "La fecha de inicio no puede ser en el futuro"}, 400

    if hora_fin < hora_inicio:
        return {"error": "La fecha de fin no puede ser anterior a la fecha de inicio"}, 400

    if cancha is None:
        return {"error": "Cancha no encontrada"}, 404

    cancha_activa = cancha.get('activa')

    if not cancha_activa:
        return {"error": "La cancha no está activa"}, 400

    if hora_inicio.minute != 0 or hora_inicio.second != 0:
        return {"error": "Los horarios deben ser en punto"}, 400

    if hora_fin.minute != 0 or hora_fin.second != 0:
        return {"error": "Los horarios deben ser en punto"}, 400

    duracion = (hora_fin - hora_inicio).total_seconds() / 3600
    if duracion < 1 or duracion > 3:
        return {"error": "La duración de la reserva debe ser entre 1 y 3 horas"}, 400

    if hora_inicio.hour < 8 or hora_fin.hour > 23:
        return {"error": "Los horarios deben estar entre las 8:00 y las 23:00"}, 400

    if hora_fin.hour == 23:
        return {"error": "La reserva no puede terminar después de las 23:00 hs"}, 400

    #buscar si la cancha ya está reservada en ese rango horario
    cancha_ocupada = reservas_repo.buscar_reserva_cancha_en_horario(id_cancha, hora_inicio, hora_fin)

    if cancha_ocupada:
        return {"error": "La cancha ya se encuentra reservada en ese horario"}, 400

    #buscar si el socio ya tiene otra reserva en ese mismo rango horario

    socio_ocupado = reservas_repo.buscar_reserva_socio_en_horario(id_socio, hora_inicio, hora_fin)

    if socio_ocupado:
        return {"error": "El socio ya tiene una reserva en ese rango horario"}, 400

    #obtener el precio por hora de la cancha
    precio_por_hora = cancha.get('precio_hora')
    total = precio_por_hora * duracion
        
    # guarda en la base de datos la reserva
    reservas_repo.guardar_reserva(id_socio, id_cancha, hora_inicio, hora_fin, total, estado="confirmada")
    return {"mensaje": "Reserva creada exitosamente"}, 201