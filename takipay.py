# São paulo
# kleberlopeskebim@gmail.com
# 00552340871
# Kleber Lopes
# 61983638888
from selenium import webdriver
import numpy_financial as npf
from selenium.webdriver.common.by import By
from time import sleep
import sqlite3
from datetime import date

def formatar_dinheiro(price):
    price = price.replace('R', '')
    price = price.replace('$', '')
    price = price.replace('.', '')
    price = price.replace(',', '.')
    price = float(price)
    return price

def calcula_taxa(total,lista): #converte o webelement em uma lista,filtrado somente o interessante e armazenando em um dicionario com as taxas calculadas
    filtro = ['FORMA', 'DE', 'PAGAMENTO', 'Cartão', 'de', 'Crédito', 'de', 'R$', 'Cupom', 'de', 'desconto', 'Aplicar',
              'PROSSEGUIR', 'PARA', 'PAGAMENTO', '*', 'Custo', 'da', 'operação', 'de', '2,95%', 'a.m.', 'aplicável',
              'para', 'parcelamento', 'em', '12x.', 'Para', 'demais', 'parcelas,', 'consulte.', '**', 'Não', 'Cobramos',
              'Taxa', 'de', 'Despachante']
    filtrado = [i for i in lista if i not in filtro]
    indice = [i for i in range(0, 23) if i % 2 == 0]

    for i in indice:
        filtrado[i] = filtrado[i][:-1]
    lista2 = [formatar_dinheiro(i) for i in filtrado]
    for i in indice:
        taxas[lista2[i]] = round(npf.rate(lista2[i], lista2[i + 1] * (-1), total, 0) * 100, 2) #armazena em um dicionario com a chave sendo a qtd de parcelas e o valor a taxa mensal
    return taxas

def db_insert(concorrente,em1x, em2x,em3x,em4x,em5x,em6x,em7x,em8x,em9x,em10x,em11x,em12x,today):
    return """INSERT INTO TAXAS VALUES ('{}', {}, {},{},{},{},{},{},{},{},{},{},{},null,null,'{}')""".format(concorrente, em1x, em2x, em3x, em4x, em5x, em6x, em7x, em8x, em9x, em10x, em11x, em12x, today)



taxas = {}
conc = 'TAKIPAY'
url = "https://www.takipay.com.br/"
email = 'kleberlopeskebim@gmail.com'
renavam = '00552340871'
first_name = 'Kleber'
last_name = 'Lopes'
phone = '61983638888'


con = sqlite3.connect('db_taxas.db')
cur = con.cursor()
today = date.today()
today = today.strftime("%d/%m/%Y")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
sleep(5)

driver.get(url)
sleep(5)
driver.find_element(By.ID, "form-field-email").send_keys(email)
driver.find_element(By.ID, "form-field-renavam").send_keys(renavam)
driver.find_element(By.XPATH, '//*[@id="taki_pay_home"]/div/div[7]/button/span/span[2]').click()
sleep(10)
driver.find_element(By.ID, "form-field-nome").send_keys(first_name)
driver.find_element(By.ID, "form-field-sobrenome").send_keys(last_name)
driver.find_element(By.ID, "form-field-telefone").send_keys(phone)
driver.find_element(By.XPATH, '/html/body/div[2]/div/div/section[2]/div/div/div/div/div/div[3]/div/form/div/div[13]/button/span/span[2]').click()
sleep(10)
driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/ul/span').click()
valor = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[1]/div[2]/span[2]')
div = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]')
taxas = calcula_taxa(formatar_dinheiro(valor.text), div.text.split())
sql = db_insert(conc, taxas[1.0], taxas[2.0], taxas[3.0], taxas[4.0], taxas[5.0], taxas[6.0], taxas[7.0], taxas[8.0],
                taxas[9.0], taxas[10.0], taxas[11.0], taxas[12.0], today)
cur.execute(sql)
con.commit()
con.close()
