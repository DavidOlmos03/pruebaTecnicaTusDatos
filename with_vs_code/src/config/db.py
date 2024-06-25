# Para trabajar con mongodb
from pymongo import MongoClient

client = MongoClient('localhost')
db = client['pruebaTusDatos']

procesos = db['procesos']
detalles = db['detalles']
actuaciones = db['actuaciones']