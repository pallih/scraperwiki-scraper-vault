import scraperwiki
import lxml.html
     
pagina_en_html = scraperwiki.scrape("http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias")
arbol = lxml.html.fromstring(pagina_en_html)

cambio = arbol.cssselect('td.tne10')
print len(cambio)
data = {
    'id' : 1,
    'cambio' : cambio[6].text_content(),
    'link' : 'http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias'
}
print data
scraperwiki.sqlite.save(['id'],data) 

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print data

import scraperwiki
import lxml.html
     
pagina_en_html = scraperwiki.scrape("http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias")
arbol = lxml.html.fromstring(pagina_en_html)

cambio = arbol.cssselect('td.tne10')
print len(cambio)
data = {
    'id' : 1,
    'cambio' : cambio[6].text_content(),
    'link' : 'http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias'
}
print data
scraperwiki.sqlite.save(['id'],data) 

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print data

