from src.config import db
from sqlalchemy import text

#SOFIII----
def buscar_socio_por_id(id):
    sql = text("""
    SELECT id, nombre, email, activo 
    FROM socios 
    WHERE id = :id
    """)
    resultado = db.session.execute(sql, {"id": id}).mappings().first() #mappings() devuelve la fila como un diccionario. first() devuelve la primera de las filas que devuelve mapping(), y si no existe la fila, devuelve None. 
    return resultado

def buscar_email_otro_socio(id, email):
    sql = text("""
    SELECT id, nombre, email, activo 
    FROM socios 
    WHERE email = :email AND id != :id
    """)
    resultado = db.session.execute(sql, {"email": email, "id": id}).mappings().first()
    return resultado

#EUGEE-----
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

def editar_socio(id, modificaciones):
    cambios = []
    parametros = {"id": id}

    if "nombre" in modificaciones:
        cambios.append("nombre = :nombre")
        parametros["nombre"] = modificaciones["nombre"]

    if "email" in modificaciones:
        cambios.append("email = :email")
        parametros["email"] = modificaciones["email"]

    if "activo" in modificaciones:
        cambios.append("activo = :activo")
        parametros["activo"] = modificaciones["activo"]

    if not cambios:
        return

    sql = text(f"""
        UPDATE socios
        SET {", ".join(cambios)}
        WHERE id = :id
    """)

    db.session.execute(sql, parametros)
    db.session.commit()
