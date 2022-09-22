
from selenium import webdriver
import numpy_financial as npf
from selenium.webdriver.common.by import By
from time import sleep
import sqlite3
from datetime import date
con = sqlite3.connect('db_taxas.db')
cur = con.cursor()
dicio = {}
today = date.today()
today = today.strftime("%d/%m/%Y")
conc = "ZAPAY"
url = "https://usezapay.com.br/"
placa = '******'
email = '***@gmail.com'
def formatar_dinheiro(price):
    price = price.replace('R', '')
    price = price.replace('$', '')
    price = price.replace('.', '')
    price = price.replace(',', '.')
    price = float(price)
    return price


def calcula_taxa(total,lista):
    filtro = ['de', 'R$', '-', 'Acréscimo:', 'RECOMENDADO']
    filtrado = [i for i in lista if i not in filtro]
    indice = [i for i in range(0, 53) if i % 4 == 0]

    for i in indice:
        filtrado[i] = filtrado[i][:-1]
    filtrado = filtrado[:54]
    lista2 = [formatar_dinheiro(i) for i in filtrado]
    for i in indice:
        dicio[lista2[i]] = round(npf.rate(lista2[i], lista2[i + 1] * (-1), total, 0) * 100, 2)
    return dicio

def db_insert(concorrente,em1x,em2x,em3x,em4x,em5x,em6x,em7x,em8x,em9x,em10x,em11x,em12x,em16x,em18x,today):
    return """INSERT INTO TAXAS VALUES ('{}',{},{},{},{},{},{},{},{},{},{},{},{},{},{},'{}')"""\
        .format(concorrente, em1x, em2x, em3x, em4x, em5x, em6x, em7x, em8x, em9x, em10x, em11x, em12x, em16x, em18x, today)


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
sleep(5)

driver.get(url)
sleep(5)

driver.find_element(By.XPATH, '//*[@id="hs-eu-confirmation-button"]').click()
sleep(5)
driver.find_element(By.NAME, "service.licensePlate").send_keys(placa)
driver.find_element(By.NAME, 'customer.email').send_keys(email)
sleep(5)
driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div/div/form/button').click()
sleep(10)
div2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div[3]/div[2]')
valor = driver.find_element(By.CLASS_NAME, 'text-primary')
taxas = calcula_taxa(formatar_dinheiro(valor.text),div2.text.split())
sql = db_insert(conc, taxas[1.0], taxas[2.0], taxas[3.0], taxas[4.0], taxas[5.0], taxas[6.0], taxas[7.0], taxas[8.0],
                taxas[9.0], taxas[10.0], taxas[11.0], taxas[12.0], taxas[16.0], taxas[18.0], today)
cur.execute(sql)
con.commit()
con.close()


