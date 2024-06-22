from selenium import webdriver
import random 
from time import sleep
import multiprocessing
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from process import identify_process, obtain_all_process, count_view_process
from details import recorrer_vistas



# Se establece el tipo de proceso a realizar
# type_process = [1,2]
# Código del demandante o demandado
# Demandante1 = 0968599020001
# Demandante2 = 0992339411001

# Demandado1 = 1791251237001
# Demandado2 = 0968599020001
# codigos_demandante = ['0968599020001','0992339411001']
# codigos_demandado = ['1791251237001','0968599020001']

def perform_query(codigo,type_process):
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

    # Conexión con la página web a "scrapear"
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)
    driver.get('https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros')

    try:
        #   Se distingue el tipo de consulta a realizar 
        #       1. Actor / Ofendido   
        #       2.  Demandado / Procesado
        identify_process(type_process, driver, codigo)


        #   Se obtiene y posteriormente se da click en el boton buscar para realizar la consulta
        boton_buscar = driver.find_element(By.XPATH,"//button[@type = 'submit']")
        boton_buscar.click()


        #   Se da tiempo para que la página cargue correctamente
        sleep(random.uniform(8.0,10.0))


        #   Se obtiene el limite de iteraciones   
        limit = count_view_process(driver)


        #   Se obtienen todos los procesos y se envian a la base de datos en mongodb
        obtain_all_process(limit, driver)

        #   Se retorna a la vista inicial
        boton_inicio = driver.find_element(By.XPATH,"//button[@aria-label='Primera página']")
        boton_inicio.click()

        #   Se espera a que la página cargue por completo
        sleep(random.uniform(8.0,10.0))

        #   Se realiza el contenido por todas las vistas, se va ingresando a cada uno de los procesos, obteniendo sus detalles 
        #   y enviandolos a la base de datos en mongodb
        recorrer_vistas(limit, driver)

        driver.quit()
    except StaleElementReferenceException:
        sleep(random.uniform(3.0,5.0))
        #listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))



if __name__ == '__main__':
    multiprocessing.freeze_support()
    codigos_demandante = ['0968599020001','0992339411001']

    # Crear los procesos en paralelo
    processes = []
    for codigo in codigos_demandante:
        type_process = 1
        p = multiprocessing.Process(target=perform_query, args=(codigo,type_process))
        processes.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for process in processes:
        process.join()

    print("Todas las consultas se han completado.")