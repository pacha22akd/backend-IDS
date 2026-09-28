from src.config import db
from sqlalchemy import text

def obtener_reservas(id_cancha, id_socio, estado, fecha_desde, fecha_hasta, limit, offset):

    sql = """ SELECT id, id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total FROM reservas WHERE 1 = 1 """
    parametros = {}

    if id_cancha is not None:
        sql += " AND id_cancha = :id_cancha "
        parametros["id_cancha"] = id_cancha

    if id_socio is not None:
        sql += " AND id_socio = :id_socio "
        parametros["id_socio"] = id_socio

    if estado is not None:
        sql += " AND estado = :estado "
        parametros["estado"] = estado

    if fecha_desde is not None:
        sql += " AND DATE(fecha_hora_inicio) >= :fecha_desde "
        parametros["fecha_desde"] = fecha_desde

    if fecha_hasta is not None:
        sql += " AND DATE(fecha_hora_inicio) <= :fecha_hasta "
        parametros["fecha_hasta"] = fecha_hasta

    sql += " ORDER BY id ASC " 
    sql += " LIMIT :limit OFFSET :offset "

    parametros["limit"] = limit
    parametros["offset"] = offset

    resultado = db.session.execute(
        text(sql),
        parametros
    )

    return [dict(row) for row in resultado.mappings().all()]

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
def guardar_reserva(id_socio, id_cancha, hora_inicio, hora_fin, total, estado="confirmada"):
    sql = text("""
        INSERT INTO reservas (id_socio, id_cancha, inicio, fin, total, estado)
        VALUES (:id_socio, :id_cancha, :inicio, :fin, :total, :estado)
    """)
    
    db.session.execute(sql, {
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "inicio": hora_inicio,
        "fin": hora_fin,
        "total": total,
        "estado": estado
    })
    db.session.commit()

    def obtener_todas_las_reservas () -> list[dict]:
        sql = text("SELECT nombre, id, id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, estado ENUM, precio_hora, precio_total FROM reservas")
        resultado = db.session.execute(sql).mappings().all()

    return [dict(fila) for fila in resultado] 

    from src.config import db

def buscar_reserva_por_id(id_reserva: int):
    sql = text("""
        SELECT id, id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total
        FROM reservas
        WHERE id = :id_reserva
    """)
    resultado = db.session.execute(sql, {"id_reserva": id_reserva}).mappings().first()
    if resultado:
        return dict(resultado)
    return None


def actualizar_estado_reserva(id_reserva: int, nuevo_estado: str):
    sql = text("""
        UPDATE reservas
        SET estado = :nuevo_estado
        WHERE id = :id_reserva
    """)
    db.session.execute(sql, {
        "nuevo_estado": nuevo_estado,
        "id_reserva": id_reserva
    })
    db.session.commit()

    return buscar_reserva_por_id(id_reserva) 