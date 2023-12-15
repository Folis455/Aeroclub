from app.models.transacciones import Transacciones
from app.models.tipo_pago import TipoPago
from app import db
from flask import jsonify

# Una Cuenta Corriente no se deberá deshabilitar, a su vez tampoco se podrá crear, se inicializará con el valor de una transacción...

class TransaccionesController:

    def _init_(self):
        pass

    def __chequearTipoPago(self,tipoPago):

        tipos=["Cheque","Efectivo", "Transferencia"] 

        print(f"__chequearTipoPago tipoPago entro: {tipoPago}")

        resultado = [x for x in tipos if x==tipoPago]

        if resultado:
            return True

        else:
            return False
    

    """ def crearTransaccion(self, monto, fecha, motivo,tipoPago,idCuentaCorriente):

             try:
                #chequeando el tipo de pago 
                if self.__chequearTipoPago(self.__chequearTipoPago,tipoPago):

                    ##aca me traigo el tipoPago para obtener su id    
                    # tipoPagoDictionary = db.session.query(TipoPago).filter_by(tipo=tipoPago).first()

                    # transaccion = Transacciones(None,monto,fecha,motivo,tipoPagoDictionary.id_tipo_pago,idCuentaCorriente)

                else:
                    return False  
              
             except Exception as ex:
                print(ex)
                return False """
    
    # ¿Para qué sirve el chequear el tipo de pago?
    # Esta funciona ignorando lo del tipo de pago...
    def crearTransaccion(self, data): 
        transaccion = Transacciones(**data)
        db.session.add(transaccion)
        db.session.commit()

        return True
    
    #Esta es solo de prueba para ver si funciona lo de borrar en cascada
    """def eliminarTransaccion(self, id):

            try:
                    #chequeando el tipo de pago 
              
                    transaccion = db.session.query(Transacciones).filter_by(id_transacciones=id).first()
                    
                    db.session.delete(transaccion)
                    db.session.commit()

                    return True 
              
            except Exception as ex:
                print(ex)
                return False"""
            
    def eliminarTransaccion(self, id_transaccion):
        try:
            transaccion = Transacciones.query.get(id_transaccion)
            
            if transaccion:
                db.session.delete(transaccion)
                db.session.commit()
                return jsonify({'message': 'Transaccion deleted successfully'})
            else:
                return jsonify({'message': 'Transaccion not found'}), 404
            
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'An error occurred', 'success': False})
        
    def obtenerTransacciones(self):
        transacciones = Transacciones.query.all()
        transaccion_list = []

        for transaccion in transacciones:
             
             transaccion_data = {
                'id_transacciones': transaccion.id_transacciones,
                'monto': transaccion.monto,
                'fecha': transaccion.fecha,
                'motivo': transaccion.motivo,
                'tipo_pago_id': transaccion.tipo_pago_id,
                'cuenta_corriente_id': transaccion.cuenta_corriente_id,
            }
             transaccion_list.append(transaccion_data)
        return jsonify(transaccion_list)
    

    # Obtener una sola transaccion (la última) de un usuario según su id
    """def obtener_transaccion(self, cuenta_corriente_id):
        transaccion_uid = Transacciones.query.filter_by(cuenta_corriente_id=cuenta_corriente_id).order_by(Transacciones.fecha.desc()).first()
        if transaccion_uid:
            transaccion_data = {
                    'id_transacciones': transaccion_uid.id_transacciones,
                    'monto': transaccion_uid.monto,
                    'fecha': transaccion_uid.fecha,
                    'motivo': transaccion_uid.motivo,
                    'tipo_pago_id': transaccion_uid.tipo_pago_id,
                    'cuenta_corriente_id': transaccion_uid.cuenta_corriente_id,
                }
            return transaccion_data 
        return False"""
    

    # Obtener todas las transacciones de un usuario según su id
    def obtener_transaccion(self, cuenta_corriente_id):
        transaccion_uid = Transacciones.query.filter_by(cuenta_corriente_id=cuenta_corriente_id)
        transaccion_uid_list = []

        for transaccion in transaccion_uid:   
             transaccion_data = {
                'id_transacciones': transaccion.id_transacciones,
                'monto': transaccion.monto,
                'fecha': transaccion.fecha,
                'motivo': transaccion.motivo,
                'tipo_pago_id': transaccion.tipo_pago_id,
                'cuenta_corriente_id': transaccion.cuenta_corriente_id,
            }
             transaccion_uid_list.append(transaccion_data)
        return transaccion_uid_list
           