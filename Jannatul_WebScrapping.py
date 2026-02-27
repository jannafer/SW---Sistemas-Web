import base64
import os
import time

import requests
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

metodo = 'POST'
uri = "https://http-repaso.appspot.com/processForm"
cabeceras = {'Host': "http-repaso.appspot.com",
             'Filename':"/processForm",
             'Content-Type': "application/x-www-form-urlencoded"}
cuerpo="erantzuna=a&erantzuna=b&erantzuna=c"

#cuerpo_encoded = urllib.parse.urlencode(cuerpo)
#cabeceras['Content-Lenght'] = str(len(cuerpo_encoded))
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=True)
codigo = respuesta.status_code
print(str(codigo) + ' ' + respuesta.reason)
for cabecera in respuesta.headers:
    print(cabecera + ': ' + respuesta.headers[cabecera])

#abrir el navegador
options=Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
browser = webdriver.Firefox(options=options)

uri = respuesta.url
browser.get(uri)
time.sleep(2)

html = browser.page_source
browser.close()

ref_doc = BeautifulSoup(html, 'html.parser') #apunta a raiz del arbol
ref_divs = ref_doc.find_all('div')
for idx, each in enumerate(ref_divs):
    ref_img = each.img                      #acceder a la imagen dentro del div
    aux = ref_img['src']                    #obtener imagen codificada o enclace a la imagen
    print(idx, each)

    if aux.find("data:image/png") != -1: #imagen codificada en base64
        img_encoded = aux.split(",")[1]
        img = base64.b64decode(img_encoded) #imagen en binario

    # hacer peticiones http para  descargar las imagenes  enlazadas
    elif aux.find("http") != -1: #imagen enlazada
        respuesta = requests.get(aux) #ddescargar la imagen
        img = respuesta.content

    else:                               #el resto de casos, no interesan
        continue
    file = open('imagenHTTP.png', 'wb')
    file.write(img)
    file.close()