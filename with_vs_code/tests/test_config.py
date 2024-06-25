import requests
import pytest
from pymongo import MongoClient, errors
#from ..src.config.config import MONGO_URI, WEB_SITE_URL

WEB_SITE_URL = 'https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros'
MONGO_URI = 'mongodb://localhost:27017/'

#   Test para la conexión con la página web
def test_connection():
    response = requests.get(WEB_SITE_URL)
    # Verificar que la URL responde con un código de estado 200 (OK)
    assert response.status_code == 200

#   Prueba la ejecución de MongoDB
def test_mongodb_client():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        
        # Esto intentará conectarse al servidor de MongoDB
        # Fuerza una llamada para verificar la conexión
        client.server_info()  
        assert True

    except errors.ServerSelectionTimeoutError as err:
        pytest.fail(f"Could not connect to MongoDB: {err}")
    

if __name__ == '__main__':
    pytest.main()
    