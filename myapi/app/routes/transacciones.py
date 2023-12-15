from flask import Blueprint, request, jsonify
from app.models.transacciones import Transacciones
from app import db
from app.utils.Security import Security
from app.controllers.transacciones import TransaccionesController
# Test
from app.models.cuenta_corriente import CuentaCorriente

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


# Esta asume que una cuenta corriente siempre tendrá un mismo ID que su Usuario, ya que al generar cada usuario,
# se genera con su cuenta corriente y deberían ir a la par...
"""@transacciones_bp.route('<int:cuenta_corriente_id>', methods=['GET'])
def get_transacciones_id(cuenta_corriente_id): 
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:

            transaccion_controller = TransaccionesController()
            transacciones = transaccion_controller.obtener_transaccion(cuenta_corriente_id)
            if transacciones:
                return jsonify({'response': transacciones, 'success': True})
            else:
                return jsonify({'message': 'No se encontraron transacciones en esta cuenta corriente.', 'success': False})
                  
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ERROR', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401   """

# Esta opción nos permite usar el id del usuario, pero como en la tabla de transacciones no tenemos el usuario_id, deberemos de 
# pedírselo a la tabla de CuentaCorriente, está mal hecho pero peor sería tener que volver a modificar la BDD.

@transacciones_bp.route('<int:usuario_id>', methods=['GET'])
def get_transacciones_usuario(usuario_id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            # buscar la cuenta corriente asociada a ese usuario
            cuenta_corriente = CuentaCorriente.query.filter_by(usuarios_id=usuario_id).first()

            if cuenta_corriente:
                transaccion_controller = TransaccionesController()
                # Usar el ID de la cuenta corriente para obtener las transacciones
                transacciones = transaccion_controller.obtener_transaccion(cuenta_corriente.id_cuenta_corriente)
                
                if transacciones:
                    return jsonify({'response': transacciones, 'success': True})
                else:
                    return jsonify({'message': 'No se encontraron transacciones para este usuario', 'success': False})
            else:
                return jsonify({'message': 'No se encontró la cuenta corriente para este usuario', 'success': False})
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ERROR', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
