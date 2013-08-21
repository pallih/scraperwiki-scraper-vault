import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.elmundo.es/elmundo/noticias-mas-leidas.html")
root = lxml.html.fromstring(html)
els = root.cssselect('div.listanoticias ol li a')
news = []
i = 0
for el in els:
    i += 1
    print i    
    print el.text_content()
    data = {
        'Order': i,
        'Header': el.text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['Order'], data=data)
      



