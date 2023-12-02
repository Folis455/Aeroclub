from flask import Blueprint, request, jsonify
from app.controllers.roles import RolesController
from app.utils.Security import Security
from app.controllers.usuarios import UsuariosController

roles_bp = Blueprint('roles', __name__)


# es necesario el email del usuario y en los datos tiene que ir los roles que debe tener
@roles_bp.route('/', methods=['POST'])
def agregar_rol():
  
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
                data = request.get_json()
                rolesController = RolesController()
                respuesta = rolesController.editarRol(data)
                if respuesta == 1:
                    return jsonify({'mensaje': 'Ese rol no esta permitido'})
                if respuesta == 2:
                    return jsonify({'mensaje': 'Ya posee ese rol'})
                if respuesta == 3:
                    return jsonify({'mensaje': 'El rol se le asigno correctamente'})
                if respuesta == 4:
                    return jsonify({'message': 'El mail no es válido y no esta asociado a una cuenta'})
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ocurrio un error', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    

# Ruta para "borrar" un usuario por email
@roles_bp.route('/', methods=['DELETE'])
def delete_rol():
  
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
                data = request.get_json()
                rolesController = RolesController()
                respuesta = rolesController.eliminarRol(data)
                if respuesta == 1:
                    return jsonify({'mensaje': 'Ese rol no esta permitido'})
                if respuesta == 2:
                    return jsonify({'mensaje': 'Se elimino el rol correctamente'})
                if respuesta == 3:
                    return jsonify({'mensaje': 'El rol que quiere eliminar no lo posee, asi que no se realiza acciones'})
                if respuesta == 4:
                    return jsonify({'message': 'El mail no es válido y no esta asociado a una cuenta'})
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ocurrio un error', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    