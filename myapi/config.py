import os
from dotenv import load_dotenv

 # Carga las variables de entorno desde el archivo .env
load_dotenv()

    # Ahora puedes acceder a las variables de entorno como si estuvieran definidas en el sistema
sqlalch_db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
secret_key = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True