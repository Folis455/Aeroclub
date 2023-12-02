from app.models.user_model import Usuarios
#from app.models.user_roles import Roles
#from app.models.user_tiene_roles import UsuarioTieneRoles
from app.controllers.cuentaCorrienteController import cuentaCorrienteController
from sqlalchemy.orm import joinedload
from app import db
from flask import jsonify


class UsuariosController:
    
    def __init__(self):
        pass 
    """
    def obtenerUsuarioPorEmail(self,mail):

        # Cargar la relación 'roles' utilizando joinedload
        #userMalFormato = db.session.query(Usuarios).filter(Usuarios.email == mail).options(joinedload(Usuarios.roles)).first()

        userMalFormato = db.session.execute(db.select(Usuarios).filter_by(email=mail)).scalar_one()
        #usuario = db.session.query(Usuarios).filter(Usuarios.email == mail)
   
        if not userMalFormato:
       
            return  False
        
        # Cargar la relación 'roles' utilizando joinedload
        userMalFormato = db.session.query(Usuarios).filter_by(email=mail).options(joinedload(Usuarios.roles)).first()

        usuario = {'id_usuarios': userMalFormato.id_usuarios, 
                    'nombre': userMalFormato.nombre,
                    'apellido': userMalFormato.apellido,
                    'email': userMalFormato.email,
                    'telefono': userMalFormato.telefono,
                    'dni': userMalFormato.dni,
                    'fecha_alta': userMalFormato.fecha_alta,
                    'fecha_baja': userMalFormato.fecha_baja,
                    'direccion': userMalFormato.direccion,
                    'foto_perfil': userMalFormato.foto_perfil,
                    'estado_hab_des': userMalFormato.estado_hab_des 
                    }
        # Include the 'roles' relationship data
        if userMalFormato.roles:
            usuario['roles'] = [
                {
                    'id_roles': role.id_roles,
                    'tipo': role.tipo,
                }
                for role in userMalFormato.roles
            ]

        return usuario
    """

    def obtenerUsuarioPorEmail(self,mail):

        # Cargar la relación 'roles' utilizando joinedload
        #userMalFormato = db.session.query(Usuarios).filter(Usuarios.email == mail).options(joinedload(Usuarios.roles)).first()

        #userMalFormato = db.session.execute(db.select(Usuarios).filter_by(email=mail)).scalar_one()
        #usuario = db.session.query(Usuarios).filter(Usuarios.email == mail)
   
         # Cargar la relación 'roles' utilizando joinedload
        userMalFormato = db.session.query(Usuarios).filter_by(email=mail).options(joinedload(Usuarios.roles), joinedload(Usuarios.cuenta_corriente)).first()

        if not userMalFormato:
       
            return  False   

        usuario = {'id_usuarios': userMalFormato.id_usuarios, 
                    'nombre': userMalFormato.nombre,
                    'apellido': userMalFormato.apellido,
                    'email': userMalFormato.email,
                    'telefono': userMalFormato.telefono,
                    'dni': userMalFormato.dni,
                    'fecha_alta': userMalFormato.fecha_alta,
                    'fecha_baja': userMalFormato.fecha_baja,
                    'direccion': userMalFormato.direccion,
                    'foto_perfil': userMalFormato.foto_perfil,
                    'estado_hab_des': userMalFormato.estado_hab_des,
                    'cuenta_corriente': {
                    'saldo_cuenta': userMalFormato.cuenta_corriente.saldo_cuenta,
                    },
                    'roles': [
                    {
                        'id_roles': role.id_roles,
                        'tipo': role.tipo,
                    }
                    for role in userMalFormato.roles
                ] 
                     
                    }
        """
        # Include the 'roles' relationship data
        if userMalFormato.roles:
            usuario['roles'] = [
                {
                    'id_roles': role.id_roles,
                    'tipo': role.tipo,
                }
                for role in userMalFormato.roles
            ]
        
        else:
            userMalFormato.roles = []
        """
        return usuario

    def obtenerUsuarios(self):
        # Cargar la relación 'roles' utilizando joinedload
        users = db.session.query(Usuarios).options(joinedload(Usuarios.roles), joinedload(Usuarios.cuenta_corriente)).all()

        users = Usuarios.query.all()
        user_list = [{'id_usuarios': user.id_usuarios, 
                        'nombre': user.nombre,
                        'apellido': user.apellido,
                        'email': user.email,
                        'telefono': user.telefono,
                        'dni': user.dni,
                        'fecha_alta': user.fecha_alta,
                        'fecha_baja': user.fecha_baja,
                        'direccion': user.direccion,
                        'foto_perfil': user.foto_perfil,
                        'estado_hab_des': user.estado_hab_des,
                        'cuenta_corriente': {
                        'saldo_cuenta': user.cuenta_corriente.saldo_cuenta,
                        },
                        'roles': [
                    {
                        'id_roles': role.id_roles,
                        'tipo': role.tipo,
                    }
                    for role in user.roles
                ]  # Incluye los datos de la relación 'roles' 
                    } for user in users if user.estado_hab_des != 0]
        return jsonify(user_list)
        

    def crearUsuario(self, data):
           
            id_usuarios = data.get('id_usuarios')
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            email = data.get('email')
            telefono = data.get('telefono')
            dni = data.get('dni')
            fecha_alta = data.get('fecha_alta')
            fecha_baja = data.get('fecha_baja')
            direccion = data.get('direccion')
            foto_perfil = data.get('foto_perfil')
            estado_hab_des = data.get('estado_hab_des')
            
            #hacer un control exacto de cada input para devolver el error exacto
            if not nombre or not apellido or not email or not telefono or not dni or not fecha_alta or not fecha_baja or not direccion or not foto_perfil or not estado_hab_des:
                return False

            usuario = Usuarios( id_usuarios=id_usuarios, nombre=nombre, apellido=apellido, 
                                email=email, telefono=telefono,
                                dni=dni, fecha_alta=fecha_alta, 
                                fecha_baja=fecha_baja, direccion=direccion, 
                                foto_perfil=foto_perfil, estado_hab_des=estado_hab_des)
            db.session.add(usuario)
            print("antes de hacer el commit")
            print(usuario.id_usuarios)
            db.session.commit()
            print("despues de hacer el commit")
            print(usuario.id_usuarios)
           #se crea la cuenta del usuario
            cuentaCorrienteController.crear_cuenta(cuentaCorrienteController,usuario.id_usuarios)
            
            return True

    def editarUsuario(self, email, data):
       
        #solo trae el dicc y no la clase de la bd
        user = self.obtenerUsuarioPorEmail(email)
        #te trae un usuario de la bd
        usuario = Usuarios.query.get(user["id_usuarios"])

        if not usuario:
        
            return  False
        
        if 'nombre' in data:
            usuario.nombre = data['nombre']
        if 'apellido' in data:
            usuario.apellido = data['apellido']
        if 'email' in data:
            usuario.email = data['email']
        if 'telefono' in data:
            usuario.telefono = data['telefono']
        if 'dni' in data:
            usuario.dni = data['dni']
        if 'fecha_alta' in data:
            usuario.fecha_alta = data['fecha_alta']
        if 'fecha_baja' in data:
            usuario.fecha_baja = data['fecha_baja']
        if 'direccion' in data:
            usuario.direccion = data['direccion']
        if 'foto_perfil' in data:
            usuario.foto_perfil = data['foto_perfil']
        if 'estado_hab_des' in data:
            usuario.estado_hab_des = data['estado_hab_des']

        #para que te lo guarde primero hay que buscar en la db una clase del modelo
        #y despues cuando modifique un atributo de esa clase cuenta como que lo modifique 
        #y ahi el commit me lo toma como un cambio y lo guarda
        db.session.commit()
        return True
 
        

    def eliminarUsuario(self, email):
        
            user = self.obtenerUsuarioPorEmail(email)
            #te trae un usuario de la bd
            usuario = Usuarios.query.get(user["id_usuarios"])
        
            if not Usuarios:
            
                return  False
            #para "borrarlo"
            usuario.estado_hab_des = 0

            db.session.commit()
            return True
        