from db import actuaciones
import random 
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


#   Función para guardar las actuaciones judiciales en la base de datos
def enviar_actuaciones(numero_proceso, listado_actuaciones):
    for actuacion in listado_actuaciones:
        #fecha_ingreso = detalle.find_element('xpath','.//')
        titulo_detalle = actuacion.find_element('xpath','.//span[contains(@class, \"title\")]').text
        
        actuaciones.insert_one({
            'titulo_detalle': titulo_detalle,
            'numero_proceso': numero_proceso
        })


#   Función para obtener las actuaciones de un proceso
def obtencion_actuaciones(proceso, driver):
    #try:
        # Se espera unos segundos antes de dar click al boton de detalles
        sleep(random.uniform(8.0,10.0))
        #listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
        
        numero_proceso = proceso.find_element(By.XPATH,'.//div[@class="numero-proceso"]').text
        boton_proceso = proceso.find_element(By.XPATH,'.//a[@href="/movimientos"]')
        boton_proceso.click()

        # Se espera unos segundos antes de dar click al boton de detalles
        #sleep(random.uniform(8.0,10.0))
        boton_detalle_proceso = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'.//a[@href="/actuaciones"]')))
        boton_detalle_proceso.click()
        # Se extraen todos los detalles según la fecha de ingreso
        #listado_detalles = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class = 'cabecera-tabla')]")))
        listado_actuaciones = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, \"mat-content\")]")))

        # Se envian los detalles a la base de datos
        enviar_actuaciones(numero_proceso,listado_actuaciones)


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
            sleep(random.uniform(3.0,5.0))
            obtencion_actuaciones(listado_procesos[i], driver)

            sleep(random.uniform(3.0,5.0))
            driver.back()
            driver.back()
            
        except StaleElementReferenceException:
            sleep(random.uniform(3.0,5.0))
            listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))


def recorrer_vistas(limit, driver):
    num_vista = 1
    sleep(random.uniform(3.0,5.0))
    listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))

    for i in range(limit):
        listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
        recorrido_por_vista(num_vista, listado_procesos, driver)
        
        num_vista += 1