from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Usal"]
mycol = mydb["scrapping"]


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
#options.add_argument('--headless')

driver_path ='C:\\Users\\david\\Documents\\chromedriver.exe'
driver = webdriver.Chrome(driver_path, options=options)
driver.get("https://www.tiempo.com")

# cerrar ventana emergente dando a "Aceptar"
WebDriverWait(driver, 5)\
	.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
										'input#sendOpGdpr')))\
	.click()
time.sleep(1)
#inserción de "Irún" en el cuadro de busqueda
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'input#buscador')))\
    .send_keys('Irun')
# dar a Irun entre los resultados
WebDriverWait(driver, 5)\
	.until(EC.element_to_be_clickable((By.XPATH,
										'/html/body/div[1]/header/aside/div/div/ul/li[1]/span[2]/span[1]')))\
	.click()

# selección de historico 
WebDriverWait(driver, 5)\
	.until(EC.element_to_be_clickable((By.XPATH,
										'/html/body/span[3]/span[1]/span/span[3]/aside/ul[1]/li[3]/a')))\
	.click()
time.sleep(1)
# selección de Resumen Mensual.
WebDriverWait(driver, 5)\
	.until(EC.element_to_be_clickable((By.XPATH,
										'/html/body/div[1]/main/div[2]/div[3]/div/div/div[4]/div/span[4]')))\
	.click()
time.sleep(1)

#seleccion cuadro calendario.
WebDriverWait(driver, 5)\
	.until(EC.element_to_be_clickable((By.XPATH,
										'/html/body/div[1]/main/div[2]/div[3]/div/div/div[5]/div[2]/span')))\
	.click()

#selecion flecha atrás calendario una vez abierto.
WebDriverWait(driver,5)\
	.until(EC.element_to_be_clickable((By.XPATH,
										'/html/body/div[1]/main/div[2]/div[3]/div/div/div[5]/div[2]/div[2]/div/a[1]')))\
	.click()

#seleccion del mes de enero 2020.
WebDriverWait(driver, 5)\
	.until(EC.element_to_be_clickable((By.XPATH,
										'/html/body/div[1]/main/div[2]/div[3]/div/div/div[5]/div[2]/div[2]/table/tbody/tr[1]/td[1]')))\
	.click()
time.sleep(1)


listamedidas = list()
tdias = list()
tmedia = list()
tmax= list()
tminima = list()
vmedia_viento = list()
rachasMax = list()
presionMedia = list()
lluvia = list()

#bucle for para recorrer cada columna y cada fila de la tabla.guarda los valores en una lista.
for dias in range(1,32):
	cuentadias =driver.find_element_by_xpath(f'/html/body/div[1]/main/div[2]/div[3]/div/div/div[5]/div[2]/table/tbody/tr[{dias}]/td[{1}]')
	cuentadias = cuentadias.text
	
	for medidas in range(1,9):
		cuentamedidas = driver.find_element_by_xpath(f'/html/body/div[1]/main/div[2]/div[3]/div/div/div[5]/div[2]/table/tbody/tr[{dias}]/td[{medidas}]')
		cuentamedidas = cuentamedidas.text
		listamedidas.append(cuentamedidas)

for i in range(0, len(listamedidas),8):
	tdias.append(listamedidas[i])
	tmedia.append(listamedidas[i+1])
	tmax.append(listamedidas[i+2])
	tminima.append(listamedidas[i+3])
	vmedia_viento.append(listamedidas[i+4])
	rachasMax.append(listamedidas[i+5])
	presionMedia.append(listamedidas[i+6])
	lluvia.append(listamedidas[i+7])
df = pd.DataFrame({'Dias': tdias, 'T.Media': tmedia, 'Temp.Máx': tmax, 'tminima': tminima, 'vmedia_viento ':vmedia_viento, 'rachasMax': rachasMax, 'presionMedia':presionMedia ,'lluvia':lluvia})
print(df)

df.to_csv('tiempo_Enero_2020bis.csv', index=False)

print(listamedidas)
