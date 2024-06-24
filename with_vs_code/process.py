from db import col
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random 
from time import sleep

# Funciones para PROCESS

def identify_process(type_process, driver, codigo):
    #   Distinción entre tipo de proceso
    if type_process == 1:
        input_user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname = 'cedulaActor']")))
        input_user.send_keys(codigo)
    elif type_process == 2:
        input_user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname = 'cedulaDemandado']")))
        input_user.send_keys(codigo)


def send_process(listado_proceso, codigo):
    for proceso in listado_proceso:
        id_proceso = proceso.find_element('xpath','.//div[@class="id"]').text
        fecha = proceso.find_element('xpath','.//div[@class="fecha"]').text
        numero_proceso = proceso.find_element('xpath','.//div[@class="numero-proceso"]').text
        accion_infraccion = proceso.find_element('xpath','.//div[@class="accion-infraccion"]').text
        
        #   Se envia la información obtenida a la base de datos
        col.insert_one({
            'doc_persona': codigo,
            'id':id_proceso,
            'fecha': fecha,
            'numero_proceso': numero_proceso,
            'accion_infraccion': accion_infraccion
        })

def count_view_process(driver):
    attempts = 0
    max_attempts = 3  # Número máximo de intentos
    while attempts < max_attempts:
        #   Se controla la excepción en caso de que la página no cargue correctamente y no se pueda obtener el elemento page_label
        try:
            # Se obtiene el número limite para realizar los cambios de página
            page_label = driver.find_element(By.XPATH, "//div[@class = 'mat-mdc-paginator-range-label']")
            text = page_label.text

            # Se utiliza la funcion split para obtener un array por palabra del texto obtenido y luego se obtiene el ultimo registro
            parts = text.split()
            limit = int(parts[len(parts) - 1])
            return limit
        except:
            # Incrementar el número de intentos
            attempts += 1
            
            # Recargar la página
            driver.refresh()
            
            # Si se han agotado los intentos, salir del bucle
            if attempts == max_attempts:
                break


def obtain_all_process(limit, driver, codigo):
    #   Obtengo el listado de procesos esperando antes 10 segundos para dar tiempo de que se carguen por completo
    listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
    
    #   Se envia la lista de procesos encontrados por pantalla a la base de datos
    send_process(listado_procesos, codigo)

    #   Se obtiene el boton de paso
    boton_paso = driver.find_element(By.XPATH,"//button[@aria-label='Página siguiente']")
                                                            
    #   Se recorren todas las vistas de los registros
    for i in range(limit-1):
        
            #   click al boton de paso
            boton_paso.click()
            
            #   Espero a que se cargue la nueva página
            sleep(random.uniform(8.0,10.0))
            
            #   Obtengo el listado de procesos esperando antes 10 segundos para dar tiempo de que se carguen por completo
            listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
            
            #   Se envia la lista de procesos encontrados por pantalla a la base de datos
            send_process(listado_procesos, codigo)
                
            #   Espero a que se cargue la nueva página
            sleep(random.uniform(8.0,10.0))
            #   Se obtiene el boton de paso
            boton_paso = driver.find_element(By.XPATH,"//button[@aria-label='Página siguiente']")