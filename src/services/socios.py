from src.validators import socios as socios_val
from src.repositories import socios as socios_repo

def registrar_nuevo_socio(datos):
    error_validacion = socios_val.validacion_socio(datos)
    if error_validacion:
        return {"error": error_validacion}, 400  # Bad Request

    email_limpio = datos.get('email').strip().lower()
    nombre = datos.get('nombre').strip()

    if socios_repo.buscar_email(email_limpio):
        return {"error": "El correo electrónico ya se encuentra registrado."}, 409
    
    socios_repo.insertar_socio(nombre, email_limpio)
    return {"mensaje": "Socio creado con éxito"}, 201

def listar_socios(args):
    try:
        limit = int(args.get('limit', 10))
    except ValueError:
        limit = 10
    
    if limit < 1:
        limit = 1
    elif limit > 100:
        limit = 100
    
    try:
        offset = int(args.get('offset', 0))
    except ValueError:
        offset = 0
    
    if offset < 0:
        offset = 0

    filtro_nombre = args.get('nombre', None)
    socios = socios_repo.obtener_socios_paginados(limit, offset, filtro_nombre)

    base_url = "/socios"
    param_filtro = f"&nombre={filtro_nombre}" if filtro_nombre else ""
    links = {
        "self": f"{base_url}?limit={limit}&offset={offset}{param_filtro}",
        "first": f"{base_url}?limit={limit}&offset=0{param_filtro}",
        "prev": f"{base_url}?limit={limit}&offset={max(0, offset - limit)}{param_filtro}" if offset > 0 else None,
        "next": f"{base_url}?limit={limit}&offset={offset + limit}{param_filtro}" if len(socios) == limit else None,
        {base_url}?limit={limit}&offset={offset}{param_filtro}"
    }

    # 6. Devolvemos los datos con una clave descriptiva y el objeto _links
    return {
        "socios": socios,
        "_links": links
    }, 200