from flask import Blueprint, request, jsonify
from app.models.aeronave_models import Aeronaves
from app import db
from app.utils.Security import Security
from app.controllers.aeronaves import AeronavesController

aeronaves_bp = Blueprint('aeronaves', __name__)

@aeronaves_bp.route('/', methods=['GET'])
def get_aeronaves():

    has_access = Security.verify_token(request.headers)

    if has_access:
        try:

            aeronave_controller = AeronavesController()
            return aeronave_controller.obtenerAeronaves()
        
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ERROR', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401        

@aeronaves_bp.route('/<matricula>', methods=['GET'])
def get_aeronave_by_matricula(matricula):
    try:
        aeronave_controller = AeronavesController()
        return aeronave_controller.obtenerAeronavePorMatricula(matricula)
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'ERROR', 'success': False})

@aeronaves_bp.route('/', methods=['POST'])
def create_aeronave():
    try:
        data = request.get_json()
        aeronave_controller = AeronavesController()
        respuesta = aeronave_controller.crearAeronave(data)
        if respuesta:
            return jsonify({'message': 'Aeronave created successfully'}), 201
        else:
            return jsonify({'message': 'Some data is invalid'}), 400
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'An error occurred', 'success': False})

@aeronaves_bp.route('/<matricula>', methods=['PATCH'])
def update_aeronave(matricula):
    try:
        data = request.get_json()
        aeronave_controller = AeronavesController()
        respuesta = aeronave_controller.editarAeronave(matricula, data)
        if respuesta:
            return jsonify({'message': 'Aeronave updated successfully'})
        else:
            return jsonify({'message': 'Aeronave not found'}), 404
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'An error occurred', 'success': False})

@aeronaves_bp.route('/<matricula>', methods=['DELETE'])
def delete_aeronave(matricula):
    try:
        aeronave_controller = AeronavesController()
        respuesta = aeronave_controller.eliminarAeronave(matricula)
        if respuesta:
            return jsonify({'message': 'Aeronave deleted successfully'})
        else:
            return jsonify({'message': 'Aeronave not found'}), 404
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'An error occurred', 'success': False})