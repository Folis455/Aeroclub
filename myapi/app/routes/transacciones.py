from flask import Blueprint, request, jsonify
from app.models.transacciones import Transacciones
from app import db
from app.utils.Security import Security
from app.controllers.transacciones import TransaccionesController

transacciones_bp = Blueprint('transacciones', __name__)

@transacciones_bp.route('/', methods=['GET'])
def get_transacciones(): 
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:

            transaccion_controller = TransaccionesController()
            return transaccion_controller.obtenerTransacciones()
        
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ERROR', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401      

@transacciones_bp.route('/', methods=['POST'])
def create_transaccion():
    try:
        data = request.get_json()
        transaccion_controller = TransaccionesController()
        respuesta = transaccion_controller.crearTransaccion(data)
        ## respuesta = transaccion_controller.crearTransaccion(monto, fecha, motivo,tipoPago,idCuentaCorriente)
        if respuesta:
            return jsonify({'message': 'Transaccion created successfully'}), 201
        else:
            return jsonify({'message': 'Some data is invalid'}), 400
    except Exception as ex:
        print(ex)
        return jsonify({'message': 'An error occurred', 'success': False})

@transacciones_bp.route('/<int:id_transaccion>', methods=['DELETE'])
def delete_transaccion(id_transaccion):
    try:
        transaccion_controller = TransaccionesController()
        respuesta = transaccion_controller.eliminarTransaccion(id_transaccion)
        return respuesta

    except Exception as ex:
        print(ex)
        return jsonify({'message': 'An error occurred', 'success': False})