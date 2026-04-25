# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# MÃ³dulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost

from pymongo import MongoClient

# Descomentar el db_client local o remoto correspondiente

# Base de datos local MongoDB

#db_client = MongoClient().local


# Base de datos remota MongoDB Atlas (https://mongodb.com)
db_client = MongoClient(
    "mongodb+srv://sergio:sdg81164@cluster0.eyvfcs3.mongodb.net/?appName=Cluster0").test