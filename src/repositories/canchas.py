from src.config import db
from sqlalchemy import text

def buscar_cancha_por_id(id_cancha):
    sql = text("SELECT * FROM canchas WHERE id = :id_cancha")
    resultado = db.session.execute(sql, {"id_cancha": id_cancha}).mappings().first()
    return dict(resultado) if resultado else None