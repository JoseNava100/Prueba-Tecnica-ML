import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

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
