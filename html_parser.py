from bs4 import BeautifulSoup 

html_fichero = open("html_parser.html", 'r')
html_codigo = html_fichero.read() # leer el contenido del fichero
html_fichero.close()

print("Analisis del HTML...")
documento = BeautifulSoup(html_codigo, 'html.parser')

imagen1 = documento.html.body.ul.li.a.img
print(imagen1)
imagen1_enlace = imagen1['src']
print(imagen1_enlace)
print('\n')

lista_imagenes = documento.find_all('img')
print(len(lista_imagenes))
for imagen in lista_imagenes:
    imagen_enlace = imagen['src']
    print(imagen_enlace)
print('\n')

lista_imagenes = documento.find_all('img', {'id': 'egela'})
imagen = lista_imagenes[0]
print(imagen)
imagen_enlace = lista_imagenes[0]['src'] 
print(imagen_enlace)
print('\n')

print (imagen.parent)
print( documento.body.ul.li.text)


# ¿Qué hace imagen.attrs?

# Busca únicamente los elementos <li> que no tengan atributos.

# Obtenga todas las imágenes (<img>) que estén dentro de esos <li>.

# Muestre por pantalla la URL (src) de cada imagen encontrada.

