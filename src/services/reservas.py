from datetime import datetime
from src.repositories import socios as socios_repo
from src.repositories import canchas as canchas_repo
from src.repositories import reservas as reservas_repo
from src.routes.socios import crear_respuesta_error, crear_errores

def listar_reservas(
    id_cancha,
    id_socio,
    estado,
    fecha_desde,
    fecha_hasta,
    limit,
    offset
):  
    if id_cancha is not None and id_cancha <= 0:
        raise ValueError("El id de cancha debe ser positivo")

    if id_socio is not None and id_socio <= 0:
        raise ValueError("El id de socio debe ser positivo")

    if limit < 1 or limit > 100:
        raise ValueError("_limit debe estar entre 1 y 100")

    if offset < 0:
        raise ValueError("_offset debe ser mayor o igual a 0")

    if ((fecha_desde is not None) and (fecha_hasta is not None) and (fecha_desde > fecha_hasta)):
        raise ValueError("fecha_desde no puede ser mayor que fecha_hasta")

    return reservas_repo.obtener_reservas(
        id_cancha,
        id_socio,
        estado,
        fecha_desde,
        fecha_hasta,
        limit,
        offset
    )

def crear_reserva(datos):

    id_socio = datos.get('id_socio')
    id_cancha = datos.get('id_cancha')
    inicio = datos.get('fecha_hora_inicio') or datos.get('inicio')
    fin = datos.get('fecha_hora_fin') or datos.get('fin')
    socio = socios_repo.buscar_socio_por_id(id_socio)
    cancha = canchas_repo.buscar_cancha_por_id(id_cancha)
    
    
   

    if not all([id_socio, id_cancha, inicio, fin]):
            return crear_respuesta_error("Faltan datos requeridos", 400)
    
    
    if socio is None:
        return crear_respuesta_error("Socio no encontrado", 404)

    try:    
        hora_inicio = datetime.fromisoformat(inicio).replace(tzinfo=None)  # Asegurarse de que la fecha y hora estén en formato naive (sin zona horaria)
        hora_fin = datetime.fromisoformat(fin).replace(tzinfo=None)  # Asegurarse de que la fecha y hora estén en formato naive (sin zona horaria)
    except (ValueError, TypeError):
        return crear_respuesta_error("Formato de fecha u hora inválido. Debe ser ISO 8601", 400)

    actividad = socio.get('activo')

    if not actividad:
        return crear_respuesta_error("El socio no está activo", 400)

    if hora_inicio < datetime.now():
        return crear_respuesta_error("La fecha de inicio no puede ser en el futuro", 400)

    if hora_fin < hora_inicio:
        return crear_respuesta_error("La fecha de fin no puede ser anterior a la fecha de inicio", 400)

    if cancha is None:
        return crear_respuesta_error("Cancha no encontrada", 404)

    cancha_activa = cancha.get('activa')

    if not cancha_activa:
        return crear_respuesta_error("La cancha no está activa", 400)

    if hora_inicio.minute != 0 or hora_inicio.second != 0:
        return crear_respuesta_error("Los horarios deben ser en punto", 400)

    if hora_fin.minute != 0 or hora_fin.second != 0:
        return crear_respuesta_error("Los horarios deben ser en punto", 400)

    duracion = (hora_fin - hora_inicio).total_seconds() / 3600
    if duracion < 1 or duracion > 3:
        return crear_respuesta_error("La duración de la reserva debe ser entre 1 y 3 horas", 400)

    if hora_inicio.hour < 8 or hora_fin.hour > 23:
        return crear_respuesta_error("Los horarios deben estar entre las 8:00 y las 23:00", 400)


    cancha_ocupada = reservas_repo.buscar_reserva_cancha_en_horario(id_cancha, hora_inicio, hora_fin)

    if cancha_ocupada:
        return crear_respuesta_error("La cancha ya se encuentra reservada en ese horario", 400)

    
    socio_ocupado = reservas_repo.buscar_reserva_socio_en_horario(id_socio, hora_inicio, hora_fin)

    if socio_ocupado:
        return crear_respuesta_error("El socio ya tiene una reserva en ese rango horario", 400)

    
    precio_por_hora = cancha.get('precio_hora')
    total = precio_por_hora * duracion
        
    reservas_repo.guardar_reserva(id_socio, id_cancha, hora_inicio, hora_fin, total, estado="confirmada")
    return None, 201
