from flask import jsonify
from app import db
from canchas import Cancha 

def obtener_cancha(cancha_id):
    cancha = Cancha.query.get(cancha_id)
    if not cancha:
        return jsonify({"mensaje": "Cancha no encontrada"}), 404
        
    return jsonify(cancha.to_dict()), 200


def actualizar_cancha_parcial(cancha_id, datos):
    cancha = Cancha.query.get(cancha_id)
    
    if not cancha:
        return jsonify({"mensaje": "Cancha no encontrada"}), 404

    
    if 'id_deporte' in datos or 'deporte' in datos:
        return jsonify({"mensaje": "No se puede modificar el deporte de una cancha existente"}), 400

    
    if 'precio' in datos and datos['precio'] <= 0:
        return jsonify({"mensaje": "El precio debe ser mayor a 0"}), 400

    
    for clave, valor in datos.items():
        if hasattr(cancha, clave) and clave not in ['id_deporte', 'deporte']:
            setattr(cancha, clave, valor)
            
    db.session.commit()
    
    return jsonify(cancha.to_dict()), 200


def consultar_disponibles(args):
    fecha = args.get('fecha')
    hora = args.get('hora')
    
    if not fecha or not hora:
        return jsonify({"mensaje": "Faltan parámetros: se requiere fecha y hora"}), 400
        

    canchas = Cancha.query.filter_by(habilitada=True).all()
    
    return jsonify([c.to_dict() for c in canchas]), 200