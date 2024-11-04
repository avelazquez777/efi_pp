from datetime import timedelta
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from app import db
from models import User
from schemas import UserSchema, MinimalUserSchema
import re

auth_bp = Blueprint('auth', __name__)

# Función para validar la contraseña
def is_valid_password(password):
    # Verifica que la contraseña tenga entre 6 y 12 caracteres, al menos un número, al menos una letra y no tenga espacios
    if (6 <= len(password) <= 12 and 
            re.search(r"[A-Za-z]", password) and 
            re.search(r"[0-9]", password) and 
            " " not in password):
        return True
    return False

# Ruta para login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.authorization
    if not data or not data.username or not data.password:
        return jsonify({"Mensaje": "Credenciales incompletas"}), 400

    username = data.username
    password = data.password

    usuario = User.query.filter_by(username=username).first()

    if usuario and check_password_hash(usuario.password_hash, password):
        # Generar el token de acceso con un tiempo de expiración de 20 minutos
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=20),
            additional_claims={"administrador": usuario.is_admin}
        )
        return jsonify({"Token": f"Bearer {access_token}"})

    return jsonify({"Mensaje": "El usuario y la contraseña no coinciden"}), 401


# Ruta para listar o crear usuarios
@auth_bp.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    # Si es un POST y es administrador, puede crear usuarios
    if request.method == 'POST':
        if administrador is True:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')  
            is_admin = data.get('is_admin') 

            # Validar los datos usando UserSchema
            data_validation = {
                "username": username,
                "password_hash": password  # Asegúrate de que esto se llame correctamente
            }
            errors = UserSchema().validate(data_validation)
            if errors:
                return jsonify(errors), 400  # Devuelve los errores si los hay

            # Verifica si el nombre de usuario ya existe
            if User.query.filter_by(username=username).first():
                return jsonify({"Mensaje": "El nombre de usuario ya existe."}), 400

            # Validar la contraseña
            if not is_valid_password(password):
                return jsonify({"Mensaje": "La contraseña debe tener entre 6 y 12 caracteres, contener al menos un número y una letra, y no tener espacios."}), 400

            try:
                # Crear un nuevo usuario
                nuevo_usuario = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    is_admin=is_admin,
                )
                db.session.add(nuevo_usuario)
                db.session.commit()

                # Usa UserSchema para serializar el usuario creado
                return jsonify({
                    "Mensaje": "Usuario creado correctamente",
                    "Usuario": UserSchema().dump(nuevo_usuario)  # Serializa el nuevo usuario
                }), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    "Mensaje": "Fallo la creación del nuevo usuario",
                    "Error": str(e)
                }), 500
        else:
            return jsonify({"Mensaje": "Solo el admin puede crear nuevos usuarios"}), 403

    # Si es un GET, cualquier usuario puede ver la lista de usuarios
    usuarios = User.query.all()
    if administrador is True:
        return UserSchema().dump(usuarios, many=True), 200
    else:
        return MinimalUserSchema().dump(usuarios, many=True), 200
