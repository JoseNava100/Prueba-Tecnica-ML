import mysql.connector
from dotenv import load_dotenv
import os

# Función simple para crear la conexion a la base de datos de acuerdo a las variables de entorno dadas
load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
