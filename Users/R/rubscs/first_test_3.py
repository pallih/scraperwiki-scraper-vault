# -*- coding: utf-8 -*-
import scraperwiki  
import lxml.html

#11870
'''
Lista de clases
Cada empresa está contenida en ss vcard
class="sswi cx" contiene nombre de la empresa (class="url" ) y telefono (class="tel"> )
class="sswe cx" contiene 
class="street-address" contiene la direccion. Esta dentro de <div class="i-extra"> 
'''
#Bucle que recorre cada pagina de la busqueda
nPaginas = 2
for i in range(1,nPaginas+1):
    if i==1:
        web = "http://11870.com/k/es/es/madrid/centro/universidad"
    else:
        web = "http://11870.com/k/es/es/madrid/centro/universidad/page"+str(i)
    print " Extrayendo de "+web+" ..."
        

    #Importo la pagina web entera         
    html = scraperwiki.scrape(web)
    #print html
    
    #Importo datos con ciertas caracteristicas en la variable data
    
    root = lxml.html.fromstring(html)
    for empresa in root.cssselect("div.ss"):       
        ''' Lo siguiente no funciona cuando un dato no existe
        nombre = empresa.cssselect("a.url")[0].text 
        telefono = empresa.cssselect("p.tel")[0].text
        direccion = empresa.cssselect("span.street-address")[0].text
        '''
   
        for nombre in empresa.cssselect("a.url"):    
            print nombre.text.encode('latin-1')
            a=0    
        for telefono in empresa.cssselect("p.tel"):    
            #print telefono.text
            a=0 
        for direccion in empresa.cssselect("span.street-address"):    
            #print direccion.text.encode('latin-1')
            a=0 
 
        data = {
            'nombre' : nombre.text.encode('latin-1'),
            'telefono' : telefono.text,
            'direccion' : direccion.text.encode('latin-1')
        }

        #Almaceno los datos
        scraperwiki.sqlite.save(unique_keys=['nombre'], data=data)

'''
#Importo la pagina web entera         
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")

#Importo datos con ciertas caracteristicas en la variable data
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content()),
            'year' : tds[1].text_content(),
            'letra' : tds[3].text_content()
        }
        print data

        #Almaceno los datos
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
'''
