import re
import scraperwiki
import mechanize
import urlparse
import lxml.html
from lxml import etree
import urllib2
from httplib import BadStatusLine 
import cgi
import itertools


#VARIABLES PARA FORMULARIO_INICIO DEL SCRAPER (PASO 1)
URL_INICIO= 'http://www.juntadeandalucia.es/haciendayadministracionpublica/clara/cprTramites.html'

#ASIGNAR VARIABLES PARA scrape_divs (PASO 3): para cada campo del trámite
CONTENIDO="body" 
ADMINISTRACION= "Junta de Andalucía" 
NIVEL_AP= "Comunidades Autónomas"

#PASO 3: Funcion a la que se le pasa cada pagina para escrapear
#No tocar nada, salvo para seleccionar un elemento por su posición, entre corchetes [] 
def scrape_divs(url_t):
    html = scraperwiki.scrape(url_t)
    root = lxml.html.fromstring(html)
    filas = root.cssselect(CONTENIDO)
    for fila in filas:
        record = {}
        vv2=vv3=vv4=vv5=vv6=vv7=vv8=vv9=vv10=vv11=vv12=vv13=vv14=vv15=vv16="" #Inicializo las variables


        def scrapear_campos_con_etiquetas(x,y): #función para conseguir bloques de texto con etiquetas
            if x is not None:
                for elem in x:
                    y = ''.join([etree.tostring(child) for child in list(elem)]) #parseo el nodo xpath y extraigo sus hijos 
            return y
        print url_t

        vv2 = NIVEL_AP+"##"+ADMINISTRACION+"##"+v2 #Tax_Categoria
        vv2=vv2.strip()
        vv3 = vv2+"##"+v2 #Tax_Subcategoria
        vv3=vv3.strip()

        v4 = fila.xpath('//div[@class="contenedor"]/div[@class="intro"]/p/text()') #Titulo
        if v4:
            vv4=v4[0]
            vv4= vv4[:250] + (vv4[250:] and '...')


        record['URL'] = "https://gestionesytramites.madrid.org"+url_t
        record['Administracion'] = ADMINISTRACION
        record['Tax Categoria'] = vv2
        record['Tax Subcategoria'] = vv3
        record['Titulo'] = vv4
        record['Descripcion'] = vv5
        record['Requisitos'] = vv6
        record['Procedimiento'] = vv7
        #record['Procedimiento internet'] = vv8   LO AGRUPA EN EL BLOQUE DE PROCEDIMIENTO PRESENCIAL
        record['Documentacion'] = vv9
        record['Otras informaciones'] = vv10
        record['Tasas'] = vv11
        record['Pago'] = vv12
        #record['Telefono'] = vv13
        #record['Fax'] = vv14
        record['Plazo'] = vv15
        record['Formularios'] = vv16

        #print record, '------------'
        # Se guarda en el datastore - 'URL' es la unique key

        scraperwiki.sqlite.save(["URL"], record)



#PASO 2: SE SIGUE EXTRAYENDO LOS LINKS DE LOS TRAMITES
def scrape_list(root):
    rows= root.cssselect("tr")
    for row in rows:
        table_cells=row.cssselect("td")
        if table_cells:
            table_cellsurls=table_cells[0].cssselect("a")
            url_t=table_cellsurls[0].attrib.get('href')
            scrape_divs(url_t)

#PASO 1: SE EMPIEZA AQUÍ 
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(URL_INICIO)

dict_categorias={'1-2PZ-411':"Presidencia",'1-S4LH8':"Administración Local y Relaciones Institucionales",'1-2PZ-133':"Justicia e Interior",'1-2PZ-406':"Educación, Cultura y Deporte",'1-2PZ-88':"Economía, Innovación, Ciencia y Empleo",'1-2PZ-341':"Hacienda y Administración Pública",'1-2PZ-410':"Fomento y Vivienda",'1-2PZ-243':"Agricultura, Pesca y Medio Ambiente",'1-2PZ-21':"Igualdad, Salud y Políticas Sociales",'1-2PZ-208':"Turismo y Comercio",'1-S96YJ':"Medio Ambiente y Ordenación del Territorio"}

dict_subcategorias ={'1-IR7IL':"Sancionador",'1-S183E':"Hacienda",'1-I1TTL':"Tributos",'1-S17QO':"Planes, proyectos y programas",'1-S17YV':"Unión Europea",'1-6A9PD':"Administración pública",'1-6A9PZ':"Agricultura, ganadería, caza y pesca",'1-6A9PB':"Autorizaciones y licencias",'1-BYL7X':"Calidad",'1-6A9PW':"Economía",'1-6A9QG':"Educación y cultura",'1-6A9PH':"Empleo",'1-6A9Q1':"Industria, comercio y otros servicios",'1-6A9Q6':"Investigación y tecnología",'1-6A9QD':"Justicia y seguridad",'1-6A9QS':"Medio ambiente",'1-6A9QM':"Ocio, turismo y deporte",'1-6A9QU':"Salud",'1-6A9PN':"Servicios sociales e igualdad",'1-6A9Q8':"Transporte, carreteras y vivienda",'1-6A9PK':"Voluntariado"}

for key, value in dict_categorias.items():
    for key2, value2 in dict_subcategorias.items():
        br.form = list(br.forms())[2]  # selecciono el formulario sin nombre
        control = br.form.find_control("consj")
        control2= br.form.find_control("temas")
        #print control.items
        control.value = [key]
        control2.value = [key2]
        v2=value
        v3=value2
        response = br.submit()#Envío el formulario con los valores asignados
        html = response.read()
        root = lxml.html.fromstring(html)
        # Comenzar a escrapear con la función scrape_list de arriba
        scrape_list(root)
        br.back()   # go back

