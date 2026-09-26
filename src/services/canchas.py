from app import db
from src.repositories.canchas import buscar_cancha_por_id
from canchas import Cancha

def obtener_todas_canchas(id):
    cancha = buscar_cancha_por_id(id)
    return cancha

def obtener_cancha_por_id(cancha_id):
    return Cancha.query.get(cancha_id)

def crear_cancha(datos):
    nueva = Cancha(**datos)
    db.session.add(nueva)
    db.session.commit()
    return nueva

def actualizar_cancha(cancha_id, datos):
    cancha = obtener_cancha_por_id(cancha_id)
    if cancha:
        for clave, valor in datos.items():
            setattr(cancha, clave, valor)
        db.session.commit()
    return cancha

def eliminar_cancha(cancha_id):
    cancha = obtener_cancha_por_id(cancha_id)
    if cancha:
        db.session.delete(cancha)
        db.session.commit()
    return cancha