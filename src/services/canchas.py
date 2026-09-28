from datetime import datetime, time, timedelta, timezone
from urllib.parse import urlencode

from src.repositories import canchas as canchas_repo
from src.validators import canchas as canchas_val


def listar_canchas(args, base_url):
    filtros, limit, offset = _validar_parametros_listado(args, {"_limit", "_offset", "id_deporte", "nombre", "techada", "activa"})
    canchas = canchas_repo.obtener_canchas(filtros, limit, offset)
    total = canchas_repo.contar_canchas(filtros)
    return {"canchas": canchas, "_links": _crear_links(base_url, filtros, limit, offset, total)}


def obtener_cancha_por_id(id_cancha):
    _validar_id(id_cancha)
    return canchas_repo.obtener_cancha_por_id(id_cancha)


def crear_cancha(datos):
    datos = _validar_cuerpo(datos, True)
    if not canchas_repo.deporte_existe(datos["id_deporte"]):
        raise ValueError("El deporte indicado no existe.")
    return canchas_repo.crear_cancha(datos)


def actualizar_cancha(id_cancha, datos):
    _validar_id(id_cancha)
    if not canchas_repo.obtener_cancha_por_id(id_cancha):
        return None
    datos = _validar_cuerpo(datos, False)
    canchas_repo.actualizar_cancha(id_cancha, datos)
    return canchas_repo.obtener_cancha_por_id(id_cancha)


def eliminar_cancha(id_cancha):
    _validar_id(id_cancha)
    if not canchas_repo.obtener_cancha_por_id(id_cancha):
        return "no_encontrada"
    if canchas_repo.tiene_reservas(id_cancha):
        return "con_reservas"
    canchas_repo.eliminar_cancha(id_cancha)
    return "eliminada"


def listar_canchas_disponibles(args, base_url):
    permitidos = {"fecha", "hora_inicio", "hora_fin", "id_deporte", "techada", "_limit", "_offset"}
    filtros, limit, offset = _validar_parametros_listado(args, permitidos)
    fecha, hora_inicio, hora_fin = args.get("fecha"), args.get("hora_inicio"), args.get("hora_fin")
    if not fecha or not hora_inicio or not hora_fin:
        raise ValueError("Los parámetros fecha, hora_inicio y hora_fin son obligatorios.")
    inicio, fin = _validar_intervalo(fecha, hora_inicio, hora_fin)
    canchas = canchas_repo.obtener_canchas_disponibles(inicio, fin, filtros, limit, offset)
    total = canchas_repo.contar_canchas_disponibles(inicio, fin, filtros)
    filtros.update({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin})
    return {"canchas": canchas, "_links": _crear_links(base_url, filtros, limit, offset, total)}


def _validar_parametros_listado(args, permitidos):
    desconocidos = set(args.keys()) - permitidos
    if desconocidos:
        raise ValueError(f"El parámetro '{sorted(desconocidos)[0]}' no está permitido.")
    limit = _entero_parametro(args.get("_limit", "10"), "_limit", 1, 100)
    offset = _entero_parametro(args.get("_offset", "0"), "_offset", 0)
    filtros = {}
    if "id_deporte" in args:
        filtros["id_deporte"] = _entero_parametro(args["id_deporte"], "id_deporte", 1)
    if "nombre" in args:
        filtros["nombre"] = args["nombre"]
    for campo in ("techada", "activa"):
        if campo in args:
            filtros[campo] = _booleano_parametro(args[campo], campo)
    return filtros, limit, offset


def _validar_cuerpo(datos, es_alta):
    error = canchas_val.validar_cancha(datos, es_alta)
    if error:
        raise ValueError(error)
    resultado = dict(datos)
    if es_alta:
        resultado.setdefault("techada", False)
        resultado.setdefault("activa", True)
    if "nombre" in resultado:
        resultado["nombre"] = resultado["nombre"].strip()
    return resultado


def _validar_intervalo(fecha, hora_inicio, hora_fin):
    try:
        dia = datetime.strptime(fecha, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError("fecha debe tener formato YYYY-MM-DD.")
    inicio_hora, fin_hora = _parsear_hora(hora_inicio, "hora_inicio"), _parsear_hora(hora_fin, "hora_fin")
    zona = timezone(timedelta(hours=-3))
    inicio, fin = datetime.combine(dia, inicio_hora, zona), datetime.combine(dia, fin_hora, zona)
    if inicio >= fin:
        raise ValueError("hora_inicio debe ser anterior a hora_fin.")
    if inicio_hora < time(8) or fin_hora > time(23):
        raise ValueError("El intervalo debe estar entre las 08:00 y las 23:00.")
    if (fin - inicio).total_seconds() / 3600 not in (1, 2, 3):
        raise ValueError("La duración debe ser entre una y tres horas completas.")
    if inicio <= datetime.now(zona):
        raise ValueError("El inicio del intervalo debe ser posterior al momento actual.")
    return inicio.replace(tzinfo=None), fin.replace(tzinfo=None)


def _parsear_hora(valor, campo):
    try:
        hora = datetime.strptime(valor, "%H:%M:%S").time()
    except (TypeError, ValueError):
        raise ValueError(f"{campo} debe tener formato HH:00:00.")
    if len(valor) != 8 or hora.minute != 0 or hora.second != 0:
        raise ValueError(f"{campo} debe indicar una hora en punto.")
    return hora


def _entero_parametro(valor, campo, minimo, maximo=None):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{campo} debe ser un número entero.")
    if str(numero) != str(valor) or numero < minimo or (maximo is not None and numero > maximo):
        limite = f" entre {minimo} y {maximo}" if maximo is not None else f" mayor o igual a {minimo}"
        raise ValueError(f"{campo} debe ser un entero{limite}.")
    return numero


def _booleano_parametro(valor, campo):
    if valor == "true":
        return True
    if valor == "false":
        return False
    raise ValueError(f"{campo} debe ser true o false.")


def _validar_entero(valor, campo, minimo):
    if type(valor) is not int or valor < minimo:
        raise ValueError(f"{campo} debe ser un entero mayor o igual a {minimo}.")


def _validar_id(id_cancha):
    _validar_entero(id_cancha, "id", 1)


def _crear_links(base_url, filtros, limit, offset, total):
    def enlace(desplazamiento):
        parametros = {"_limit": limit, "_offset": desplazamiento, **filtros}
        parametros = {clave: str(valor).lower() if type(valor) is bool else valor for clave, valor in parametros.items()}
        return {"href": f"{base_url}?{urlencode(parametros)}"}
    ultimo_offset = ((total - 1) // limit) * limit if total else 0
    links = {"_first": enlace(0), "_last": enlace(ultimo_offset)}
    if offset > 0:
        links["_prev"] = enlace(max(0, offset - limit))
    if offset + limit < total:
        links["_next"] = enlace(offset + limit)
    return links
