import scraperwiki
import lxml.html 

#https://scraperwiki.com/docs/python/python_css_guide/

def href_find():#function to grab hrefs
    html = scraperwiki.scrape("http://www.parcan.es/composicion/listapleno.py?LEGIS=8")
    root = lxml.html.fromstring(html)
    Lista= [];
    for el in root.cssselect("div#cuerpo tr td a"):  
            cadena = lxml.html.tostring(el)
            if cadena.find("target") >= 0 :
                if cadena.find("class") <= 0 :
                    if cadena.find("rss") <= 0 :
                        enlace = el.attrib['href']
                        Lista.append(enlace);
    return Lista;


def get_element(url):
    index = "http://www.parcan.es"
    url_diputado = ''
    url_diputado += index + url
    web = scraperwiki.scrape(url_diputado)
    elemento = lxml.html.fromstring(web)
    return elemento

#devuelve el nombre del parlamentario
def get_nombre(url):
    elemento = get_element(url)
    nombre = elemento.cssselect("td h1")
    for el in nombre:
        print el.text
    return el.text

#devuelve la isla o el grupo parlamentario en función del valor que se pase por parámetro
def get_datos(url,valor):
    elemento = get_element(url)
    conjunto = elemento.cssselect("td p a")
    tam = len(conjunto) - valor

    return conjunto[tam].text

#obtener link iniciativas
def get_link_iniciativas(url):
    elemento = get_element(url)    
    tab = elemento.cssselect("div.tabhead ul li a")
    for cm in tab:
        cadena = lxml.html.tostring(cm)
        if cadena.find("first") <= 0 :
            if cadena.find("last") <= 0 :
                return cm.attrib['href']

#obtener link intervenciones
def get_link_intervenciones(url):   
    elemento = get_element(url)    
    tab = elemento.cssselect("div.tabhead ul li a")
    for cm in tab:
        cadena = lxml.html.tostring(cm)
        if cadena.find("first") <= 0 :
            if cadena.find("last") >= 0 :
                return cm.attrib['href']

# obtener iniciativas
def get_iniciativas(url):
    Lista_iniciativas= [];
    link_iniciativas = get_link_iniciativas(url)
    index = "http://www.parcan.es/composicion/"
    url_iniciativas = ''
    url_iniciativas += index + link_iniciativas
    web_iniciativas = scraperwiki.scrape(url_iniciativas)
    element_ini = lxml.html.fromstring(web_iniciativas) 
    iniciativas = element_ini.cssselect("div.scrollbars tbody tr td a")
    for ini in iniciativas:
        Lista_iniciativas.append(ini.text)
    return Lista_iniciativas


# obtener intervenciones
def get_intervenciones(url):
    Lista_intervenciones= [];
    link_intervenciones = get_link_intervenciones(url)
    index = "http://www.parcan.es/composicion/"
    url_intervenciones = ''
    url_intervenciones += index + link_intervenciones
    web_intervenciones = scraperwiki.scrape(url_intervenciones)
    element = lxml.html.fromstring(web_intervenciones)
    intervenciones = element.cssselect("div.scrollbars tbody tr td.fecha")
    for int in intervenciones:
        Lista_intervenciones.append(int.text)
    return Lista_intervenciones


urls = href_find();
unique_key=0
for url in urls:
    nombre = get_nombre(url)
    isla = get_datos(url,2)
    cir = get_datos(url,1)
    iniciativas = get_iniciativas(url);
    intervenciones = get_intervenciones(url);
    #a partir de aquí guarda datos en bd sql_lite
    #https://scraperwiki.com/docs/python/python_datastore_guide//
    data = {}
    unique_key += 1
    data['unique_key'] =  unique_key
    data['nombre'] = nombre
    data['isla'] = isla
    data['grupo'] = cir
    data['intervenciones'] = intervenciones
    data['iniciativas'] = iniciativas   
    scraperwiki.sqlite.save(["unique_key"], data) #Almacena con identificador primario

                
                          

