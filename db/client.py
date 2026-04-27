# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# MÃ³dulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Descomentar el db_client local o remoto correspondiente

# Base de datos local MongoDB

#db_client = MongoClient().local


# Base de datos remota MongoDB Atlas (https://mongodb.com)

load_dotenv()

user     = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
host     = os.getenv("MONGO_HOST")
db_name  = os.getenv("MONGO_DB")

uri = f"mongodb+srv://{user}:{password}@{host}"

db_client = MongoClient(uri).test