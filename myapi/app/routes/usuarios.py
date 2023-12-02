from flask import Blueprint, request, jsonify
from app.utils.Security import Security
from app.controllers.usuarios import UsuariosController

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
def get_users():
    
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
           
            usuarioController = UsuariosController() 
            return usuarioController.obtenerUsuarios()
           
        except Exception as ex:
            print(ex)
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@usuarios_bp.route('/<email>', methods=['GET'])
def getUsuarioByEmail(email):

    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
           
            usuarioController = UsuariosController() 
            return jsonify(usuarioController.obtenerUsuarioPorEmail(email))
           
        except Exception as ex:
            print(ex)
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    

@usuarios_bp.route('/', methods=['POST'])
def create_user():
    
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
            data = request.get_json()
          
            usuarioController = UsuariosController() 
            respuesta = usuarioController.crearUsuario(data)
            
            if respuesta == True:
                return jsonify({'message': 'User created successfully'}), 201 
            
            else:
                return jsonify({'message': 'Algunos datos ingresados estan mal'}), 400
        
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ocurrio un error', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


# Ruta para actualizar un usuario por Email
@usuarios_bp.route('/<email>', methods=['PATCH'])
def update_user(email):
  
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
                data = request.get_json()
                usuarioControler = UsuariosController()
                respuesta = usuarioControler.editarUsuario(email, data)
                if respuesta == True:
                    return jsonify({'mensaje': 'Usuario actualizado correctamente'})
                else:
                    return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ocurrio un error', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

# Ruta para "borrar" un usuario por email
@usuarios_bp.route('/<email>', methods=['DELETE'])
def delete_usuario(email):
  
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
                usuarioControler = UsuariosController()
                respuesta = usuarioControler.eliminarUsuario(email)
                if respuesta == True:
                    return jsonify({'mensaje': 'Usuario actualizado correctamente'})
                else:
                    return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ocurrio un error', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
      
    


    

        