import scraperwiki
import lxml.html
     
pagina_en_html = scraperwiki.scrape("http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias")
arbol = lxml.html.fromstring(pagina_en_html)

cambio = arbol.cssselect('td.tne10')

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print cambio[6].text_content()
import scraperwiki
import lxml.html
     
pagina_en_html = scraperwiki.scrape("http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias")
arbol = lxml.html.fromstring(pagina_en_html)

cambio = arbol.cssselect('td.tne10')

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print cambio[6].text_content()
