import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if sys.argv[1] == 'descarga':
    fichero_html = open("html_parser_JS.html", 'r')
    codigo_html = fichero_html.read() # fitxategiaren edukia irakurri
    fichero_html.close()
    print(codigo_html)

elif sys.argv[1] == 'render':
    uri = "C:/Users/bcpalgum/Documents/pythonProject/sw2024/B2_WebScraping/html_parser_JS.html"
    browser = webdriver.Firefox() # abrir el navegador
    browser.get(uri) # abrir en el na vegador el fichero
    # <li> esperar a que se renderice
    WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
    codigo_html = browser.page_source # guardar el codigo
    browser.close()
    print(codigo_html)

print("Analizar HTML...")
documento = BeautifulSoup(codigo_html, 'html.parser')
print (documento)
elementos_li = documento.find_all('li')
for each in elementos_li:
    print(each)