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
    return "", 201

def listar_socios(args):
    parametros_permitidos = {"_limit", "_offset", "nombre", "activo"}
    for parametro in args:
        if parametro not in parametros_permitidos:
            return {
                "error": f"El parámetro '{parametro}' no está permitido."
            }, 400
    try:
        limit = int(args.get('_limit', 10))
    except ValueError:
        return {"error": "_limit debe ser un número entero"}, 400
    
    if limit < 1 or limit > 100:
        return {"error": "_limit debe ser un entero entre 1 y 100."}, 400
    
    try:
        offset = int(args.get('_offset', 0))
    except ValueError:
        return {"error": "_offset debe ser un número entero."}, 400
    
    if offset < 0:
        return {"error": "_offset debe ser mayor o igual a 0."}, 400

    filtro_nombre = args.get('nombre', None)
    filtro_activo = args.get('activo', None)
    if filtro_activo is not None:
        if filtro_activo == "true":
            filtro_activo = True

        elif filtro_activo == "false":
            filtro_activo = False

        else:
            return {
                "error": "El parámetro activo debe ser true o false."
            }, 400
        
    socios = socios_repo.obtener_socios_paginados(limit, offset, filtro_nombre, filtro_activo)
    total_socios = socios_repo.contar_socios(filtro_nombre, filtro_activo)

    if not socios:
        return None, 204

    ultimo_offset = ((total_socios - 1) // limit) * limit

    base_url = "/api/socios"
    param_filtro = ""

    if filtro_nombre:
        param_filtro += f"&nombre={filtro_nombre}"

    if filtro_activo is not None:
        param_filtro += f"&activo={'true' if filtro_activo else 'false'}"

    links = {
        "_first": {"href": f"{base_url}?_limit={limit}&_offset=0{param_filtro}"},

        "_last": {
            "href": f"{base_url}?_limit={limit}&_offset={ultimo_offset}{param_filtro}"}
    }

    if offset > 0:
        links["_prev"] = {"href": f"{base_url}?_limit={limit}&_offset={max(0, offset - limit)}{param_filtro}"}

    if offset + limit < total_socios:
        links["_next"] = {"href": f"{base_url}?_limit={limit}&_offset={offset + limit}{param_filtro}"}

    # 6. Devolvemos los datos con una clave descriptiva y el objeto _links
    return {
        "socios": socios,
        "_links": links
    }, 200

#SOFI-------

def obtener_socio_por_id(id):
    socio_buscado = socios_repo.buscar_socio_por_id(id)
    return socio_buscado

def modificar_socio(id, modificaciones):
    socio_a_modificar = obtener_socio_por_id(id)

    if socio_a_modificar is None:
        return {
            "error": "No encontrado",
            "descripcion": f"No existe el socio con id {id}."
        }

    error = socios_val.validar_modificaciones_socio(modificaciones)

    if error is not None:
        return error

    if "email" in modificaciones:
        modificaciones["email"] = modificaciones["email"].strip().lower()

    if "email" in modificaciones:
        socio_con_mismo_email = socios_repo.buscar_email_otro_socio(
            id,
            modificaciones["email"]
        )

        if socio_con_mismo_email is not None:
            return {
                "error": "Email repetido",
                "descripcion": "El email ingresado ya pertenece a otro socio."
            }

    socios_repo.editar_socio(id, modificaciones)

    return {}