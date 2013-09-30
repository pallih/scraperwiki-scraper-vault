import scraperwiki
import lxml.html

#https://scraperwiki.com/docs/python/python_css_guide/

def href_find():#function to grab hrefs
    html = scraperwiki.scrape("http://www.senado.es/web/composicionorganizacion/senadores/composicionsenado/senadoresenactivo/consultaordenalfabetico/index.html")
    root = lxml.html.fromstring(html)
    Lista= [];
    for el in root.cssselect("div.senador_ampliado a"):  
            cadena = lxml.html.tostring(el)
            #if cadena.find("target") >= 0 :
                #if cadena.find("class") <= 0 :
                    #if cadena.find("rss") <= 0 :
            enlace = el.attrib['href']
            Lista.append(enlace)
    return Lista;

def get_element(url):
    index = "http://www.senado.es"
    url_senador = ''
    url_senador += index + url
    web = scraperwiki.scrape(url_senador)
    elemento = lxml.html.fromstring(web)
    return elemento

def get_nombre(url): #nombre del senador
    elemento = get_element(url)
    nombre = elemento.cssselect("div.mod_interior h1 span meta")
    for el in nombre:
        cadena = lxml.html.tostring(el)
        if cadena.find("Nombre") >= 0 :
            nombre = el.attrib['content']
            print nombre
    return nombre

def get_dato(url, valor): #calcula la legislatura o la ciudad
    elemento = get_element(url)
    dato = elemento.cssselect("div.content_left_colum2 ul li meta")
    for el in dato:
        cadena = lxml.html.tostring(el)
        if cadena.find(valor) >= 0 :
            if cadena.find("ELECTO") <= 0 :
                dato = el.attrib['content']
                print dato
    return dato
 
def get_partido(url): #devuelve el partido político del senador
    elemento = get_element(url)
    partido = elemento.cssselect("div.content_left_colum2 ul li a meta")
    for el in partido:
        partido = lxml.html.tostring(el)
        if partido.find("Partido politico") >= 0 :
            partido = el.attrib['content']
            print partido
    return partido  



urls = href_find();
unique_key=0
for url in urls:
    nombre = get_nombre(url)
    legislatura = get_dato(url,"Legislatura")
    ciudad = get_dato(url,"Procedencia")
    cir = get_partido(url)
    #a partir de aquí guarda datos en bd sql_lite
    #https://scraperwiki.com/docs/python/python_datastore_guide//
    data = {}
    unique_key += 1
    data['unique_key'] =  unique_key
    data['nombre'] = nombre
    data['legislatura'] = legislatura;
    data['ciudad'] = ciudad
    data['partido'] = cir
    scraperwiki.sqlite.save(["unique_key"], data) #Almacena con identificador primario
import scraperwiki
import lxml.html

#https://scraperwiki.com/docs/python/python_css_guide/

def href_find():#function to grab hrefs
    html = scraperwiki.scrape("http://www.senado.es/web/composicionorganizacion/senadores/composicionsenado/senadoresenactivo/consultaordenalfabetico/index.html")
    root = lxml.html.fromstring(html)
    Lista= [];
    for el in root.cssselect("div.senador_ampliado a"):  
            cadena = lxml.html.tostring(el)
            #if cadena.find("target") >= 0 :
                #if cadena.find("class") <= 0 :
                    #if cadena.find("rss") <= 0 :
            enlace = el.attrib['href']
            Lista.append(enlace)
    return Lista;

def get_element(url):
    index = "http://www.senado.es"
    url_senador = ''
    url_senador += index + url
    web = scraperwiki.scrape(url_senador)
    elemento = lxml.html.fromstring(web)
    return elemento

def get_nombre(url): #nombre del senador
    elemento = get_element(url)
    nombre = elemento.cssselect("div.mod_interior h1 span meta")
    for el in nombre:
        cadena = lxml.html.tostring(el)
        if cadena.find("Nombre") >= 0 :
            nombre = el.attrib['content']
            print nombre
    return nombre

def get_dato(url, valor): #calcula la legislatura o la ciudad
    elemento = get_element(url)
    dato = elemento.cssselect("div.content_left_colum2 ul li meta")
    for el in dato:
        cadena = lxml.html.tostring(el)
        if cadena.find(valor) >= 0 :
            if cadena.find("ELECTO") <= 0 :
                dato = el.attrib['content']
                print dato
    return dato
 
def get_partido(url): #devuelve el partido político del senador
    elemento = get_element(url)
    partido = elemento.cssselect("div.content_left_colum2 ul li a meta")
    for el in partido:
        partido = lxml.html.tostring(el)
        if partido.find("Partido politico") >= 0 :
            partido = el.attrib['content']
            print partido
    return partido  



urls = href_find();
unique_key=0
for url in urls:
    nombre = get_nombre(url)
    legislatura = get_dato(url,"Legislatura")
    ciudad = get_dato(url,"Procedencia")
    cir = get_partido(url)
    #a partir de aquí guarda datos en bd sql_lite
    #https://scraperwiki.com/docs/python/python_datastore_guide//
    data = {}
    unique_key += 1
    data['unique_key'] =  unique_key
    data['nombre'] = nombre
    data['legislatura'] = legislatura;
    data['ciudad'] = ciudad
    data['partido'] = cir
    scraperwiki.sqlite.save(["unique_key"], data) #Almacena con identificador primario
