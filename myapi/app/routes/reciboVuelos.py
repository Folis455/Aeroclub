from flask import Blueprint, request, jsonify
from app.controllers.recibosVuelos import RecibosController 
from app.controllers.transacciones import TransaccionesController
from app.utils.Security import Security


reciboVuelos_bp = Blueprint('recibo-vuelos', __name__)

@reciboVuelos_bp.route('/<email>', methods=['GET'])
def obtenerRecibos(email):
  
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
                recibosController = RecibosController()
                respuesta = recibosController.obtenerRecibo(email)
                if respuesta == 1:
                    return jsonify({'message': 'El mail no le pertenece a un asociado', 'success': False})
                if respuesta == 2:
                    return jsonify({'message': 'El asociado no tiene recibos aún', 'success': False})

                if respuesta :
                    return jsonify({"respuesta":respuesta})
            
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ocurrio un error', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


# es necesario el email del usuario y en los datos tiene que ir los roles que debe tener
@reciboVuelos_bp.route('/', methods=['POST'])
def crear_recibos_vuelos():
  
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
                data = request.get_json()
                emailAsociado=data.get("emailAsociado")
                emailInstructor=data.get("emailInstructor") 
                emailGestor=data.get("emailGestor")
                observaciones=data.get("observaciones")
                matricula=data.get("matricula")
                fecha=data.get("fecha")
                itinerarios=data.get("itinerarios")
                recibosController = RecibosController()
                respuesta = recibosController.crearRecibo(emailAsociado,emailInstructor,emailGestor,observaciones,
                                                          matricula,fecha,itinerarios)
                
                if respuesta == 1:
                    return jsonify({'mensaje': 'El asociado que ingreso, no tiene rol de Asociado', 'success': False})
                if respuesta == 2:
                    return jsonify({'mensaje': 'El gestor que ingreso, no tiene rol de Gestor', 'success': False})
                if respuesta == 3:
                    return jsonify({'mensaje': 'El instructor que ingreso, no tiene rol de instrunctor', 'success': False})
                if respuesta == 4:
                    return jsonify({'message': 'El instructor no es valido', 'success': False})
                if respuesta == 5:
                    return jsonify({'message': 'Algún itinerario tiene un dato erroneo', 'success': False})
                if respuesta == 6:
                    return jsonify({'message': 'Algun dato del Recibo esta erroneo', 'success': False})
                if respuesta == 7:
                    return jsonify({'message': 'Hubo un error en la transacción verifique los dato y envie nuevamente', 'success': False})  
                if respuesta == 8:
                    return jsonify({'message': 'Algún dato de los itinerarios es erroneo, veifique los dato y envie nuevamente', 'success': False})
                if respuesta == 9:
                    return jsonify({'message': 'La aeronave no es válida, ingrese una matrícula válida', 'success': False})
                if respuesta == 10:
                    return jsonify({'message': 'El Asociado no es un usuario válido', 'success': False})
                if respuesta == 11:
                    return jsonify({'message': 'El Gestor no es un usuario válido', 'success': False})         
                if respuesta == 13:
                    return jsonify({'message': 'Recibo creado satisfactoriamente', 'success': True})        
            
        except Exception as ex:
            print(ex.args)
            return jsonify({'message': "error", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    

@reciboVuelos_bp.route('/transaccion', methods=['DELETE'])
def eliminarTransaccion():
  
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        try:
                data = request.get_json()
                id=data.get("id")
                
                transaccionesController = TransaccionesController()
                respuesta = transaccionesController.eliminarTransaccion(id)
                if respuesta :
                    return jsonify({"respuesta":respuesta})
                else:
                    return jsonify({"respuesta":False})
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'ocurrio un error', 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    