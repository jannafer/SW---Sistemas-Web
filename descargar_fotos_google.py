import base64
import time
from ssl import Options
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#abrir el  navegador
options=Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
browser = webdriver.Firefox(options=options)

uri="https://www.google.com/search?q=gatos&udm=2"
browser.get(uri)

for i in range(1,5):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)

html = browser.page_source
browser.close()

ref_doc=BeautifulSoup(html,"html.parser")
ref_divs=ref_doc.find_all('div',{'class':'q1MG4e mNsIhb'}) #apunta a los  divs

for idx, each in enumerate(ref_divs):
    ref_img=each.img
    aux=ref_img['src']
    print(idx,each)

    if aux.find("data:image/jpeg") != -1: #imagen codificada  en  base64
        img_encoded=aux.split(",")[1]
        img=base64.b64decode(img_encoded)
    elif aux.find("http")!=-1:   #imagen enlazada
        respuesta=requests.get(aux) #descargar la imagen
    else: #el  resto de datos no interesan
        continue

    print("bing chiling")
    os.makedirs("./imagenes", exist_ok=True)
    file=open("./imagenes/"+str(idx)+".jpeg","wb")
    file.write(img)
    file.close()
