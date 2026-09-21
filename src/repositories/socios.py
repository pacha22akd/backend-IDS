from src.config import db
from sqlalchemy import text

def buscar_email(email):
    sql = text("SELECT id, nombre, activo FROM socios WHERE email = :email")
    resultado = db.session.execute(sql, {"email": email}).fetchone()
    return resultado

def insertar_socio(nombre, email):
    sql = text("INSERT INTO socios (nombre, email, activo) VALUES (:nombre, :email, 1)")
    db.session.execute(sql, {"nombre":nombre, "email":email})
    db.session.commit()

def obtener_socios_paginados(limit, offset, filtro_nombre=None):
    query_str = "SELECT id, nombre, email, activo FROM socios WHERE 1=1"
    parametros = {"limite": limit, "desplazamiento": offset}

    if filtro_nombre:
        query_str += " AND nombre ILIKE :filtro"  # ILIKE ignora mayúsculas/minúsculas 
        parametros["filtro"] = f"%{filtro_nombre}%"

    query_str += " ORDER BY id ASC LIMIT :limite OFFSET :desplazamiento"
    resultado = db.session.execute(text(query_str), parametros)
    
    socios = [
        {
            "id": row.id,
            "nombre": row.nombre,
            "email": row.email,
            "activo": row.activo
        }
        for row in resultado
    ]
    
    return socios
