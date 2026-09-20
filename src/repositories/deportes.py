from sqlalchemy import text
from db.init_db import db

def obtener_todos_los_deportes() -> list[dict]:
    sql = text("SELECT nombre FROM deportes")
    resultado = db.session.execute(sql).mappings().all()
    
    return [dict(fila) for fila in resultado]