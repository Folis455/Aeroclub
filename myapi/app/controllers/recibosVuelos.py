from app.models.user_model import Recibos
from app.models.recibos_tipos import Recibos_tipos
from app.models.user_model import Usuarios
from app.models.aeronave_models import Aeronaves
from app.models.tarifas import Tarifas
from app.controllers.itinerarios import ItinerariosController
from app.controllers.cuentaCorrienteController import cuentaCorrienteController
from app.models.user_model import UsuariosTienenRecibos
from app.models.user_tiene_roles import UsuarioTieneRoles
from app.models.user_roles import Roles
from app.models.transacciones import Transacciones
from app.models.itinerarios_model import Itinerarios
from app.models.itinerarios_model import ItinerarioTieneCodigosAeropuertos
from app.models.itinerarios_model import CodigoAeropuerto
from app.models.itinerarioTipos import ItinerarioTipos
from app import db
from flask import jsonify
from datetime import datetime

class RecibosController:

    def _init_(self):
        pass

    def obtenerRecibo(self, emailAsociado):
        try:

            recibos=[]

            asociado = db.session.query(Usuarios).filter_by(email=emailAsociado).first()
            
            if asociado:

                asociadoTinenRecibos = db.session.query(UsuariosTienenRecibos).filter_by(usuarios_id = asociado.id_usuarios,rol='Asociado').all()
                print(asociadoTinenRecibos)

                for asociadoTieneRecibo in asociadoTinenRecibos:

                    itinerarios = []
                    
                    idRecibo = asociadoTieneRecibo.recibos_id
                    print(f"id de cada recibo: {idRecibo}")

                    recibo = db.session.query(Recibos).filter_by(id_recibos=idRecibo).first()

                    #Hay que inicializarlo para que no tire error cuando se pregunta con un if
                    #si existe 
                    #instructorTieneRecibo= None
                    instructor = None
                    aeronave = None

                    instructorTieneRecibo = db.session.query(UsuariosTienenRecibos).filter_by(recibos_id = idRecibo,rol='Instructor').first()
                    gestorTineneRecibo = db.session.query(UsuariosTienenRecibos).filter_by(recibos_id = idRecibo,rol='Gestor').first()

                    if(instructorTieneRecibo):    
                        instructor = db.session.query(Usuarios).filter_by(id_usuarios = instructorTieneRecibo.usuarios_id).first()
                        print(f"Instructor name: {idRecibo} {instructor.nombre}")

                    gestor = db.session.query(Usuarios).filter_by(id_usuarios = gestorTineneRecibo.usuarios_id).first()

                    transaccion = db.session.query(Transacciones).filter_by(id_transacciones = recibo.transacciones_id).first()

                    getAllItinerarios = db.session.query(Itinerarios).filter_by(RECIBOS_id_recibos = recibo.id_recibos).all()

                    print(f"Gestor name:{idRecibo} {gestor.nombre}") 

                    for itinerario in getAllItinerarios:

                        aeronave = db.session.query(Aeronaves).filter_by(id_aeronaves= itinerario.aeronaves_id).first()
                        
                        codsAeros = db.session.query(ItinerarioTieneCodigosAeropuertos).filter_by(itinerarios_id = itinerario.id_itinerarios).all()

                        idCodAeroLlegada =  codsAeros[0].codigos_aeropuertos_id
                        idCodAeroSalida =  codsAeros[1].codigos_aeropuertos_id

                        codAeroLlegada = db.session.query(CodigoAeropuerto).filter_by(id_codigos_aeropuertos = idCodAeroLlegada).first()
                        codAeroSalida = db.session.query(CodigoAeropuerto).filter_by(id_codigos_aeropuertos = idCodAeroSalida).first()

                        tipoItinerario = db.session.query(ItinerarioTipos).filter_by(id_tipo_itinerarios = itinerario.tipo_itinerarios_id).first()

                        dictItinerario =  {"horaSalida": itinerario.hora_salida,
                                            "codAeroSalida":codAeroSalida.codigo_aeropuerto, 
                                            "horaLlegada":itinerario.hora_llegada,
                                            "codAeroLlegada":codAeroLlegada.codigo_aeropuerto,
                                            "cantAterrizajes":itinerario.cantidad_aterrizajes,
                                            "tipoItinerario":tipoItinerario.tipo
                                            }
                        
                        print(f"Un itinerario dict: {dictItinerario}")
                        itinerarios.append(dictItinerario)

                    if instructor:

                        recibo = [{  'asociado':asociado.nombre + " " + asociado.apellido,
                                        'instructor':instructor.nombre + " " + instructor.apellido,
                                        'gestor':gestor.nombre + " " + gestor.apellido,  
                                        'precioTotal': transaccion.monto*(-1),
                                        'observaciones': recibo.observaciones,
                                        'matricula': aeronave.matricula,  
                                        }]
                        
                    else:
                        recibo = [{  'asociado':asociado.nombre + " " + asociado.apellido,
                                        'instructor':"",
                                        'gestor':gestor.nombre + " " + gestor.apellido,  
                                        'precioTotal': transaccion.monto*(-1),
                                        'observaciones': recibo.observaciones,
                                        'matricula': aeronave.matricula,  
                                        }]
                            
    
                    reciboCompleto =  recibo + itinerarios

           

                    recibos.append(reciboCompleto)    

                print(recibos)

                if recibos == []:
                    return 2

                return recibos
            else:
                return 1    
        

        except Exception as ex:
            print(ex.args)
            return 'Ocurrió un error al obtener el recibo'
    
    
    def crearRecibo(self, emailAsociado,emailInstructor, emailGestor,observaciones,
                    matricula, fecha, itinerarios):

            try:
                #las inicializo en none para que no me de error cuando esta en el catch
                #y la variable no se inicializo
                transaccionInstructor=None
                transaccionAsociado=None
                #Esta flag nos va a indicar si se ingresa algun itineraro con vuelos que
                #involucren a un Instructor y se cambiara por true, sino seguira false
                #y cuando se cree la fila en la tabla usuarios tienen recibos, ahi se
                #verificara si la flag es false no se creara la fila y si es true si
                flagSiHayVuelosConInstructor=False

                #me traigo la aeronave
                aeronave = Aeronaves.query.filter_by(matricula=matricula).first() 
                #me traigo al asociado
                asociado = db.session.query(Usuarios).filter_by(email=emailAsociado).first()
                #me traigo el instructor
                instructor = db.session.query(Usuarios).filter_by(email=emailInstructor).first()
                #me traigo al gestor
                gestor = db.session.query(Usuarios).filter_by(email=emailGestor).first()
                
                rolAsociado = db.session.query(Roles).filter_by(tipo='Asociado').first()
                asociadoTieneRol = db.session.query(UsuarioTieneRoles).filter_by(usuarios_id=asociado.id_usuarios, roles_id=rolAsociado.id_roles).first() 

                rolGestor = db.session.query(Roles).filter_by(tipo='Gestor').first()
                gestorTieneRol = db.session.query(UsuarioTieneRoles).filter_by(usuarios_id=gestor.id_usuarios, roles_id=rolGestor.id_roles).first()

                if not (asociadoTieneRol):

                    return 1
                
                if not (gestorTieneRol):

                    return 2

                if aeronave:
                    #me traigo la tarifa del avion
                    tarifa = Tarifas.query.filter_by(aeronaves_id=aeronave.id_aeronaves).first()
                    #arranco un array para guardar el precio por itinerario
                    precioItinerarios = []
                    
                    #vamos a recorrer los itinerarios para calcular todo lo que se tiene que
                    #pagar, ya que hay que calcular las horas
                    for itinerario in itinerarios:
                        print(f"itinerario: {itinerario}")
                        # Calcular la diferencia entre las dos fechas y horas
                        salida = datetime.strptime(itinerario.get('horaSalida'), "%Y-%m-%d %H:%M:%S")
                        llegada = datetime.strptime(itinerario.get('horaLlegada'), "%Y-%m-%d %H:%M:%S")
                        diferencia = -(salida - llegada)
                           
                        # Obtener la diferencia en horas como un número flotante
                        diferencia_en_horas = diferencia.total_seconds() / 3600

                        #aca se fija si hay que agregar la tariva de instruccion
                        if (itinerario.get('tipoItinerario') == "Sólo con instrucción") | (itinerario.get('tipoItinerario') == "Doble comando"):

                            print(f"tarifa: {tarifa}")

                            precioCadaItinerario = {"vuelo":tarifa.importe_vuelo*diferencia_en_horas,
                                                    "instuccion":tarifa.importe_instruccion*diferencia_en_horas} 
                            precioItinerarios.append(precioCadaItinerario)
    
                            #si algun itineriario es con instruccion pero no hay uun instructor
                            #valido entonces retorna un error
                            if instructor:
                                rolInstructor = db.session.query(Roles).filter_by(tipo='Instructor').first()
                                instructorTieneRol = db.session.query(UsuarioTieneRoles).filter_by(usuarios_id=instructor.id_usuarios, roles_id=rolInstructor.id_roles).first() 
                                

                                if instructorTieneRol:
                                  
                                    flagSiHayVuelosConInstructor=True
                                
                                else:
                                    return 3
                            else: 
                                return 4
                        else: 
                            
                            precioCadaItinerario = {"vuelo":tarifa.importe_vuelo*diferencia_en_horas,
                                                "instuccion":0} 
                            precioItinerarios.append(precioCadaItinerario)

                    #creando la fecha actual    
                    fecha_actual = datetime.now()
                    fecha= str(fecha_actual.year) + "-" + str(fecha_actual.month) + "-" + str(fecha_actual.day)

                    #lo que va a pagar en la tansaccion
                    precioTotalVuelo = 0
                    #lo que va a cobrar el instructor en la transaccion
                    valorPagoInstructor = 0

                    #ahora recorro el array en el cual cargue todos los precios de los itinerarios
                    #el valor del vuelo y el de instruccion y ahora vamos a hacer la sumatoria
                    for precioPorItinerario in precioItinerarios:

                        if precioPorItinerario.get("instuccion") > 0:
                            
                            valorPagoInstructor = valorPagoInstructor + precioPorItinerario.get("instuccion") 

                        precioTotalVuelo = precioTotalVuelo +  precioPorItinerario.get("vuelo") + precioPorItinerario.get("instuccion")

                    #para que sea negativo y se lo debite la transaccion
                    precioTotalVuelo = precioTotalVuelo*(-1)    

                    #pago del asociado
                    transaccionAsociado = cuentaCorrienteController.actualizar_saldo(cuentaCorrienteController,asociado.id_usuarios,precioTotalVuelo,fecha,"Pago de vuelo","Efectivo")
                    
                    if transaccionAsociado:
                        #traigo el tipoRecibo para usar el id
                        tipoRecibo = db.session.query(Recibos_tipos).filter_by(tipo="Recibo de Vuelo").first()
                        #Se crea un recibo
                        recibo = Recibos(None,fecha_actual,observaciones,tipoRecibo.id_tipo_recibos,transaccionAsociado.id_transacciones)

                        if instructor:

                            #pago del instructor
                            transaccionInstructor = cuentaCorrienteController.actualizar_saldo(cuentaCorrienteController,instructor.id_usuarios,valorPagoInstructor,fecha,"Pago de vuelo","Efectivo")
                
                       
                        if recibo:

                             #guardamos el recibo
                            db.session.add(recibo)
                            db.session.commit()


                            #rolAsociado = db.session.query(Roles).filter_by(tipo="Asociado").first()
                            #rolInstructor = db.session.query(Roles).filter_by(tipo="Instructor").first()
                            #rolGestor = db.session.query(Roles).filter_by(tipo="Gestor").first()
                            #realaciones de los usuarios y los recibos con el rol de cada uno
                            print(f"este es el recibo id: {recibo.id_recibos}")    
                            #creamos y guardamos la relacion de usuariostienenrecibos
                       
                            asociadoTieneRecibo = UsuariosTienenRecibos(None,recibo.id_recibos,asociado.id_usuarios,"Asociado")
                            gestorTieneRecibo = UsuariosTienenRecibos(None,recibo.id_recibos,gestor.id_usuarios,"Gestor")
                            
                            db.session.add(asociadoTieneRecibo)
                            db.session.add(gestorTieneRecibo)
                            db.session.commit()
                        
                            if (instructor and flagSiHayVuelosConInstructor):
                                #si hay un instructor tambien creamos la relacion
                                instructorTieneRecibo = UsuariosTienenRecibos(None, recibo.id_recibos,instructor.id_usuarios, "Instructor")

                                db.session.add(instructorTieneRecibo)
                                db.session.commit()
                            
                            itinerariosCreadosConSuRelacion = []
                            #por cada itinerario que se paso en la llamada de la api se creara un itinenario
                            #y se guardara
                            for itinerario in itinerarios:
                            
                                print(f"este es el itinerario : {itinerario}")                                    

                                respuestaCreacionItinerario = ItinerariosController.crearItinerario(ItinerariosController,
                                                                                            itinerario.get('horaSalida'),
                                                                                                itinerario.get('codAeroSalida'),
                                                                                                itinerario.get('horaLlegada'),
                                                                                                itinerario.get('codAeroLlegada'),
                                                                                                observaciones,
                                                                                                itinerario.get('cantAterrizajes'),
                                                                                                matricula,
                                                                                                itinerario.get('tipoItinerario'),
                                                                                                recibo.id_recibos)

                                itinerariosCreadosConSuRelacion.append(respuestaCreacionItinerario)

                            if not respuestaCreacionItinerario[0]:
                                
                                print("no se cargo algun itinerario")
                                #Aca hay que poner la logica de borrar todo lo que se inserto
                                # recibos, transacciones, la trabla de los usuarios tiene recibos, etc
                                #y a reestablecer la cuenta corriente al estado anterior
                                print(f"ENTRE a la excepcion, asociado: {asociado}")        
                                
                                if instructor:
                                    if transaccionInstructor:    
                                        montoInstructor = transaccionInstructor.monto 
                                        idCuentaCorrienteInstructor = transaccionInstructor.cuenta_corriente_id
                                        db.session.delete(transaccionInstructor)
                                        resDos = cuentaCorrienteController.retrotraer_pago(cuentaCorrienteController,montoInstructor,idCuentaCorrienteInstructor)
                                        print(f"se retrotrajo el pago del instructor: {resDos} ")

                                if asociado:
                                    if transaccionAsociado:    
                                        montoAsociado = transaccionAsociado.monto 
                                        idCuentaCorrienteAsociado = transaccionAsociado.cuenta_corriente_id                     
                                        db.session.delete(transaccionAsociado)
                                        resUno = cuentaCorrienteController.retrotraer_pago(cuentaCorrienteController,montoAsociado,idCuentaCorrienteAsociado)
                                        print(f"se retrotrajo el pago del asociado: {resUno} ")
                                db.session.commit()  
                                return 5
                                
                            return 13     
                        else:
                            return 6 

                    else:
                        return 7 
                else:
                    return 9    
           
            except Exception as ex:
                print(ex)
           
                print(f"ENTRE a la excepcion, asociado: {asociado}")  

        
                if instructor:
                    if transaccionInstructor:    
                        montoInstructor = transaccionInstructor.monto 
                        idCuentaCorrienteInstructor = transaccionInstructor.cuenta_corriente_id
                        db.session.delete(transaccionInstructor)
                        resDos = cuentaCorrienteController.retrotraer_pago(cuentaCorrienteController,montoInstructor,idCuentaCorrienteInstructor)
                        print(f"se retrotrajo el pago del instructor: {resDos} ")


                if asociado:
                    if transaccionAsociado:    
                        montoAsociado = transaccionAsociado.monto 
                        idCuentaCorrienteAsociado = transaccionAsociado.cuenta_corriente_id                     
                        db.session.delete(transaccionAsociado)
                        resUno = cuentaCorrienteController.retrotraer_pago(cuentaCorrienteController,montoAsociado,idCuentaCorrienteAsociado)
                        print(f"se retrotrajo el pago del asociado: {resUno} ")
                    db.session.commit()   

                else:
                    return 10
                
                if not gestor:
                    return 11

                
                db.session.commit()        
               
                return 8           



"""
data = {
  emailAsociado:"",
  emailInstructor: "", 
  emailGestor: "",
  observaciones: "",
  matricula: "",
  fecha:"",
  itinerarios: [
          
   {horaSalida:"",
    codAeroSalida:"", 
    horaLlegada:"",
    codAeroLlegada:"",
    cantAterrizajes:"",
    tipoItinerario:""
    } ,
     {horaSalida:"",
    codAeroSalida:"", 
    horaLlegada:"",
    codAeroLlegada:"",
    cantAterrizajes:"",
    tipoItinerario:""
    } ,
     {horaSalida:"",
    codAeroSalida:"", 
    horaLlegada:"",
    codAeroLlegada:"",
    cantAterrizajes:"",
    tipoItinerario:""
    } 
  ]     
}

INDICAR EL TIPO DE ITINERARIO:        Sólo con instrucción. (con instrucción)
                                      Doble comando. (con instrucción)
                                      Travesía
                                      Vuelo por Instrumentos bajo capota
                                      Vuelo nocturno  
"""  