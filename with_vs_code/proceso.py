from db import col
# Funciones para PROCESO
def enviar_proceso(listado_proceso):
    for proceso in listado_proceso:
        id_proceso = proceso.find_element('xpath','.//div[@class="id"]').text
        fecha = proceso.find_element('xpath','.//div[@class="fecha"]').text
        numero_proceso = proceso.find_element('xpath','.//div[@class="numero-proceso"]').text
        accion_infraccion = proceso.find_element('xpath','.//div[@class="accion-infraccion"]').text
        
        # Se envia la información obtenida a la base de datos
        col.insert_one({
            'id':id_proceso,
            'fecha': fecha,
            'numero_proceso': numero_proceso,
            'accion_infraccion': accion_infraccion
        })