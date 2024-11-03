from flask import Blueprint, request, make_response, jsonify
from app import db
from models import Equipo, Marca, Categoria
from schemas import EquipoSchema, MarcaSchema, CategoriaSchema, UserSchema, MinimalUserSchema
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
equipo_bp = Blueprint('equipos', __name__)

@equipo_bp.route('/marcas', methods=['GET'])
def marcas():
    marcas = Marca.query.all()
    return MarcaSchema().dump(marcas, many=True)

@equipo_bp.route('/categorias', methods=['GET'])
def categorias():
    categorias = Categoria.query.all()
    return CategoriaSchema().dump(categorias, many=True)

@equipo_bp.route('/equipos', methods=['GET', 'POST'])
@jwt_required()
def equipos():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')
    if request.method == "POST":
        if administrador is True:
            data = request.get_json() # Solo el administrador puede crear un equipo
            errors = EquipoSchema().validate(data)

            if errors:
                return make_response(jsonify(errors), 400)  # Retorna errores con código 400
            
            nuevo_equipo = Equipo(
                nombre=data.get('nombre'),
                costo=data.get('costo'),
                anio_fabricacion=data.get('anio_fabricacion'),
                modelo_id=data.get('modelo_id'),
                categoria_id=data.get('categoria_id'),
                proveedor_id=data.get('proveedor_id')
            )
            db.session.add(nuevo_equipo)
            db.session.commit()
            return make_response(EquipoSchema().dump(nuevo_equipo), 201)  # Retorna el nuevo equipo con código 201
        else:
            return jsonify({"Mensaje": "Solo el admin puede crear nuevos usuarios"}), 403

    equipos = Equipo.query.all()
    return EquipoSchema().dump(equipos, many=True)
