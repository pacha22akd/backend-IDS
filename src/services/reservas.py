from datetime import datetime
from src.repositories import socios as socios_repo
from src.repositories import canchas as canchas_repo
from src.repositories import reservas as reservas_repo
from src.routes.socios import crear_respuesta_error

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
        hora_fin = datetime.fromisoformat(fin).replace(tzinfo=None) #el replace se usa pq mysql usan fechas sin zona horaria
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

    from src.repositories.reservas import obtener_todas_las_reservas

def ordenar_reservas(reservas: dict) -> dict:
    return {
        "nombre": reservas["nombre"],
        "id": reservas["id"],
        "id_cancha": reservas["id_cancha"],
        "id_socio": reservas["id_socio"],
        "fecha_hora_inicio": reservas["fecha_hora_inicio"],
        "fecha_hora_fin": reservas["fecha_hora_fin"],
        "estado ENUM": reservas["estado ENUM"],
        "precio_hora": reservas["precio_hora"],
        "precio_hora": reservas["precio_hora"]
    }

def listar_reservas() -> list[dict]:
    reservas = obtener_todas_las_reservas()
    return [ordenar_reservas(d) for d in reservas]

def cambiar_estado_reserva(id_reserva, datos):
    # 1. Validar que el cuerpo contenga el estado
    if not isinstance(datos, dict) or "estado" not in datos:
        return crear_respuesta_error("El cuerpo de la solicitud debe contener el campo 'estado'", 400)
    
    nuevo_estado = datos.get("estado")
    estados_validos = {"confirmada", "cancelada", "finalizada"}
    
    if nuevo_estado not in estados_validos:
        return crear_respuesta_error("El estado ingresado no es válido", 400)

    # 2. Buscar si la reserva existe usando el repositorio
    reserva = reservas_repo.buscar_reserva_por_id(id_reserva)
    if reserva is None:
        return crear_respuesta_error("Reserva no encontrada", 404)

    estado_actual = reserva.get("estado")

    # 3. Regla: Repetir el estado actual devuelve éxito sin modificar
    if estado_actual == nuevo_estado:
        return dict(reserva), 200

    # 4. Restricción: Si ya está cancelada o finalizada, no se puede cambiar a otro estado
    if estado_actual in ["cancelada", "finalizada"]:
        return crear_respuesta_error(f"No se puede modificar una reserva en estado {estado_actual}", 409)

    ahora = datetime.now()

    # 5. Reglas de transición desde 'confirmada'
    if estado_actual == "confirmada":
        if nuevo_estado == "cancelada":
            # Condición: El horario de inicio todavía no llegó
            inicio = reserva.get("fecha_hora_inicio")
            inicio_dt = datetime.fromisoformat(str(inicio).replace('-03:00', '')) if isinstance(inicio, str) else inicio
            
            if ahora >= inicio_dt:
                return crear_respuesta_error("No se puede cancelar una reserva cuyo horario de inicio ya pasó o comenzó", 409)
                
        elif nuevo_estado == "finalizada":
            # Condición: Se alcanzó o superó el horario de finalización
            fin = reserva.get("fecha_hora_fin")
            fin_dt = datetime.fromisoformat(str(fin).replace('-03:00', '')) if isinstance(fin, str) else fin
            
            if ahora < fin_dt:
                return crear_respuesta_error("No se puede finalizar una reserva antes de su horario de fin", 409)

    # 6. Actualizar el estado en la base de datos
    reservas_repo.actualizar_estado_reserva(id_reserva, nuevo_estado)
    
    # Obtener la reserva actualizada para devolverla en la respuesta
    reserva_actualizada = reservas_repo.buscar_reserva_por_id(id_reserva)
    return dict(reserva_actualizada), 200
