import scraperwiki
import lxml.html
import time

# Blank Python

idx = 0

for i in range(1,45):
    base_url = 'http://planetafan.com/cas/site/tiendas.asp?prov=0&loc=0&pag='+str(i)
    
    html = scraperwiki.scrape(base_url)
    root = lxml.html.fromstring(html)
    links = root.cssselect("ul#listado-productos li")
    
    for link in links:

        record = {}

        name = link.cssselect("a")[0].text_content()
        address = link.cssselect("p")[0].text_content()

        #process

        address = address.replace('(','')
        address = address.replace(')','')
        address = address.replace('C/','Calle')
        #address = address.replace('Pº','Paseo')
        
        
    
        print name, address

        record['idx'] = idx
        record['name'] = name
        record['address'] = address

        scraperwiki.sqlite.save(['idx'], record)

        idx = idx + 1

    time.sleep(1)
