import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://www.tinglesa.com.uy/listado.php?idCategoria=176")
print html

import lxml.html
root = lxml.html.fromstring(html)
tcuerpo = root.cssselect("div[class='cuerpo_central_in'] tr")
for tr in root.cssselect("div[class='item_producto_gde'] "):
    nom = tr.find_class("descripcion_dep")
    prec = tr.find_class("link_mas_info")
    nom2 = nom[0].text_content().strip()
    
    data = {
            'nombre': nom2,
            'precio' : prec[0].text_content()
            #,'years_in_school' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['nombre'], data=data)

