import mysql.connector
from dotenv import load_dotenv
import os

# Cargamos las variable de entorno desde el archivo .env
load_dotenv()

# Función para obtener la conexion a la base de datos con las variables de entorno cargadas
def get_connection(with_db=True):
    config = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
    }

    if with_db:
        config["database"] = os.getenv("DB_NAME")

    return mysql.connector.connect(**config)
