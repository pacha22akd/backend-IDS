from src.config import db
from sqlalchemy import text

# 1. Buscar si el socio ya tiene reserva en ese horario
def buscar_reserva_socio_en_horario(id_socio, hora_inicio, hora_fin):
    sql = text("""
        SELECT * 
        FROM reservas 
        WHERE id_socio = :id_socio 
          AND fecha_hora_inicio < :hora_fin 
          AND fecha_hora_fin > :hora_inicio
        LIMIT 1
    """)
    
    resultado = db.session.execute(sql, {
        "id_socio": id_socio,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin
    }).mappings().first()
    
    return resultado


# 2. Buscar si la cancha ya está ocupada en ese horario
def buscar_reserva_cancha_en_horario(id_cancha, hora_inicio, hora_fin):
    sql = text("""
        SELECT * 
        FROM reservas 
        WHERE id_cancha = :id_cancha 
          AND fecha_hora_inicio < :hora_fin 
          AND fecha_hora_fin > :hora_inicio
        LIMIT 1
    """)
    
    resultado = db.session.execute(sql, {
        "id_cancha": id_cancha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin
    }).mappings().first()
    
    return resultado


# 3. Insertar la nueva reserva en MySQL
def guardar_reserva(id_socio, id_cancha, inicio, fin, total, estado="confirmada"):
    sql = text("""
        INSERT INTO reservas (id_socio, id_cancha, inicio, fin, total, estado)
        VALUES (:id_socio, :id_cancha, :inicio, :fin, :total, :estado)
    """)
    
    db.session.execute(sql, {
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "inicio": inicio,
        "fin": fin,
        "total": total,
        "estado": estado
    })
    db.session.commit()