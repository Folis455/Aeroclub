import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests 
from flask import Blueprint
from app import db
from app.utils.Security import Security

googleLogin_bp = Blueprint('googleLogin',__name__)


#app.secret_key = "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"  # Clave secreta para la aplicación Flask

# Permitir tráfico HTTP inseguro para desarrollo local
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "770670922407-2f0dh7bl39t9mgu7l6vt8gjs85srn27n.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

# Configuración del flujo de autenticación de Google
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost/callback"
)

# Función decoradora para comprobar si el usuario ha iniciado sesión
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Autorización requerida
        else:
            return function()

    return wrapper

# Ruta para la página de inicio de sesión
@googleLogin_bp.route("/google/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


# Ruta para manejar la respuesta de Google OAuth2
@googleLogin_bp.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500) 

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=10
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    return redirect("/google/confirmacion")


# Ruta de la área protegida
@googleLogin_bp.route("/google/confirmacion")
@login_is_required
def confirmacion():
    return f"¡Desea continuar el inicio con esta cuenta {session['email']} sino tiene una cuenta con este mail, se le creara automaticamente una cuenta! <br/> <a href='/google/token-jwt'><button> continuar </button></a> <a href='/google/logout'><button> Cancelar</button></a>"

# Ruta para cerrar sesión
@googleLogin_bp.route("/google/logout")
def logout():
    session.clear()
    return redirect("/google")

# Ruta de la página de inicio
@googleLogin_bp.route("/google")
def index():
    return "¡Hola Mundo! <a href='/google/login'><button>Iniciar sesión</button></a>"

# Ruta de la página de inicio
@googleLogin_bp.route("/google/token-jwt")
def jwtLogout():
   
    encoded_token = Security.generate_token(session["email"])
    
    return f"¡Hola {session['email']}! <br/> <a href='/google/logout'><button>Cerrar sesión</button></a> <br/> El token es: { encoded_token }"




