from src.repositories.deportes import obtener_todos_los_deportes

def ordenar_deporte(deporte: dict) -> dict:
    return {
        "nombre": deporte["nombre"]
    }

def listar_deportes() -> list[dict]:
    deportes = obtener_todos_los_deportes()
    return [ordenar_deporte(d) for d in deportes]
    