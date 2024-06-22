from selenium import webdriver
import random 
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from proceso import enviar_proceso

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

# Conexión con la página web a "scrapear"
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)
driver.get('https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros')

# Se establece el tipo de proceso a realizar
type_process = int(input("Desea ingresar código para: \n"+
                   "1. Demandante\n"+
                   "2. Demandado\n"))
# Código del demandante o demandado
# Demandante1 = 0968599020001
# Demandante2 = 0992339411001

# Demandado1 = 1791251237001
# Demandado2 = 0968599020001
codigo = input("Ingrese el número de identificación: ")


# Se obtiene el número limite para realizar los cambios de página
page_label = driver.find_element(By.XPATH, "//div[@class = 'mat-mdc-paginator-range-label']")
text = page_label.text

# Se utiliza la funcion split para obtener un array por palabra del texto obtenido y luego se obtiene el ultimo registro
parts = text.split()
limit = int(parts[len(parts) - 1])


# Obtengo el listado de procesos esperando antes 10 segundos para dar tiempo de que se carguen por completo
listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
# Se envia la lista de procesos encontrados por pantalla a la base de datos
# enviar_proceso(listado_procesos)

# # Ciclo para recorrer el listado de procesos y poder obtener y enviar los detalles de cada uno
# for proceso in listado_procesos:
#     try:
#         obtencion_detalle(proceso)
#     except StaleElementReferenceException:
#         # Reubicar en caso de excepción
#         listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='causa-individual ng-star-inserted']")))
#         obtencion_detalle(proceso)

# Se obtiene el boton de paso
boton_paso = driver.find_element(By.XPATH,"//button[@aria-label='Página siguiente']")
                                                           
# Se recorren todas las vistas de los registros
for i in range(4):
    try:
        # click al boton de paso
        boton_paso.click()
        # Espero a que se cargue la nueva página
        sleep(random.uniform(8.0,10.0))
        # Obtengo el listado de procesos esperando antes 10 segundos para dar tiempo de que se carguen por completo
        listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'causa-individual ng-star-inserted']")))
        # Se envia la lista de procesos encontrados por pantalla a la base de datos
        enviar_proceso(listado_procesos)
        
        # for proceso in listado_procesos:
        #     try:
        #         obtencion_detalle(proceso)
        #     except StaleElementReferenceException:
        #         # Reubicar en caso de excepción
        #         listado_procesos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='causa-individual ng-star-inserted']")))
        #         obtencion_detalle(proceso)
            
        # Espero a que se cargue la nueva página
        sleep(random.uniform(8.0,10.0))
        # Se obtiene el boton de paso
        boton_paso = driver.find_element(By.XPATH,"//button[@aria-label='Página siguiente']")
        
    except Exception as e:
        print(e)
        break