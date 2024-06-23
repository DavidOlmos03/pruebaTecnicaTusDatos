
from db import detalles
import random 
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


def enviar_detalles(numero_proceso,listado_detalles):
    for detalle in listado_detalles:
        id_detalle = detalle.find_element('xpath','.//div[@class = "numero-incidente"]').text
        fecha = detalle.find_element('xpath','.//div[@class = "fecha-ingreso"]').text
        actores_ofendidos = detalle.find_element('xpath','.//div[@class = "lista-actores"]').text
        demandados_procesados = detalle.find_element('xpath','.//div[@class = "lista-demandados"]').text
        
        
        detalles.insert_one({
            'id': id_detalle,
            'numero_proceso': numero_proceso,
            'fecha' : fecha,
            'actores_ofendidos' : actores_ofendidos,
            'demandados_procesados' : demandados_procesados
        })


#print(listado_procesos[0].text)
def obtencion_detalle(proceso, driver):
    
        # Se espera unos segundos antes de dar click al boton de detalles
        sleep(random.uniform(8.0,10.0))
        listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
        
        numero_proceso = proceso.find_element(By.XPATH,'.//div[@class="numero-proceso"]').text
        boton_proceso = proceso.find_element(By.XPATH,'.//a[@href="/movimientos"]')
        boton_proceso.click()
        
        #listado_detalles = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class = 'cabecera-tabla')]")))
        listado_detalles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, \"lista-movimiento-individual\")]")))

        # Se envian los detalles a la base de datos
        enviar_detalles(numero_proceso,listado_detalles)


def recorrido_por_vista(num_vista,listado_procesos, driver):
    for i in range(len(listado_procesos)):
        try:
            sleep(random.uniform(3.0,5.0))
            listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
            sleep(random.uniform(3.0,5.0))

            # Se obtiene el boton de paso
            boton_paso = driver.find_element(By.XPATH,"//button[@aria-label='Página siguiente']")

            # ciclo para dar click en el boton de paso las veces necesarias para llegar a la vista que necesito
            for n in range(num_vista-1) : 
                boton_paso.click()

            sleep(random.uniform(3.0,5.0))
            listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
            #boton_proceso = listado_procesos[i].find_element(By.XPATH,'.//a[@href="/movimientos"]')
            #boton_proceso.click()

            # Obtengo los detalles del proceso
            # sleep(random.uniform(3.0,5.0))
            obtencion_detalle(listado_procesos[i], driver)

            sleep(random.uniform(3.0,5.0))
            driver.back()
            
        except StaleElementReferenceException:
            sleep(random.uniform(3.0,5.0))
            listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))


def recorrer_vistas(limit, driver):
    num_vista = 1
    sleep(random.uniform(3.0,5.0))
    listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
    """
        POSIBLE ERROR:  Aqui se puede estar cortando el ciclo antes de que termine de extraer los detalles de todas las vistas
                        faltaria la ultima vista
    """
    for i in range(limit-1):
    # sleep(random.uniform(3.0,5.0))
        listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
        recorrido_por_vista(num_vista, listado_procesos, driver)

        num_vista += 1