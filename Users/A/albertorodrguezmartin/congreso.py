import scraperwiki
import lxml.html

#https://scraperwiki.com/docs/python/python_css_guide/


def url_links():
    url_ini= "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DiputadosTodasLegislaturas?_piref73_1335404_73_1335403_1335403.next_page=/wc/busquedaAlfabeticaTodasLeg&paginaActual="
    Lista= [];
    for i in range(87):
        url = ''
        url += url_ini + str(i)
        Lista.append(url);
    return Lista;
        
         
def href_find():
    urls = url_links();
    index = "http://www.congreso.es"
    for i in range(1):
        html = scraperwiki.scrape("http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados")
        root = lxml.html.fromstring(html)
        Lista= [];
        for el in root.cssselect("div.listado_1 ul li a"):  
            cadena = lxml.html.tostring(el)
            enlace = el.attrib['href']
            print enlace
            Lista.append(enlace);
    return Lista;

href_find()

