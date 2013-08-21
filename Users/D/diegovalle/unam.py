import scraperwiki        
import lxml.html
html = scraperwiki.scrape("https://escolar1.unam.mx/Junio2012/resultados/1/1010035.html")
root = lxml.html.fromstring(html)

for el in root.cssselect("body a"):           
    print el.text_content()

