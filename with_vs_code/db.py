# Para trabajar con mongodb
from pymongo import MongoClient

client = MongoClient('localhost')
db = client['pruebaTusDatos']

col = db['procesos']
detalles = db['detalles']