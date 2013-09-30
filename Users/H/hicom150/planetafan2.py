import scraperwiki
import lxml.html
from lxml.html.clean import Cleaner
import time

# Blank Python

idx = 0

def scrape_card(url):

    html = scraperwiki.scrape(url)
    html = cleaner.clean_html(html)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div#contenido p")

    if len( links[0].text_content().strip().split('\r') ) > 1:

        direccion_a = links[0].text_content().strip().split('\r')[0].strip()
        direccion_b = links[0].text_content().strip().split('\r')[1].strip()

        direccion = direccion_a + "\n" + direccion_b

    else:

        direccion = links[0].text_content().strip()

    
    telefono = "".join(links[1].text_content().split())
    fax = "".join(links[2].text_content().split())
    
    if len(links[3].cssselect("a")[0].attrib['href'])> len('http://'):

        web = links[3].cssselect("a")[0].attrib['href']

    else:
    
        web = ""

    return direccion, telefono, fax, web
    

cleaner = Cleaner()
cleaner.kill_tags = ['strong']

for i in range(1,45):
    base_url = 'http://planetafan.com/cas/site/tiendas.asp?prov=0&loc=0&pag='+str(i)
    
    html = scraperwiki.scrape(base_url)
    root = lxml.html.fromstring(html)
    links = root.cssselect("ul#listado-productos li")
    
    for link in links:

        record = {}

        name = link.cssselect("a")[0].text_content()
        card_link = link.cssselect("a")[0].attrib['href']
        address = link.cssselect("p")[0].text_content()

        direccion, telefono, fax, web = scrape_card('http://planetafan.com/cas/site/'+card_link)
        
        #process

        address = address.replace('(','')
        address = address.replace(')','')
        address = address.replace('C/','Calle')
        address = address.replace('C\\','Calle')
        #address = address.replace('Pº','Paseo')
    
        print direccion, telefono, fax, web

        record['idx'] = idx
        record['name'] = name
        record['address'] = address
        record['address_display'] = direccion
        record['phone'] = telefono
        record['fax'] = fax
        record['web'] = web

        scraperwiki.sqlite.save(['idx'], record)

        idx = idx + 1
        
    time.sleep(1)
import scraperwiki
import lxml.html
from lxml.html.clean import Cleaner
import time

# Blank Python

idx = 0

def scrape_card(url):

    html = scraperwiki.scrape(url)
    html = cleaner.clean_html(html)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div#contenido p")

    if len( links[0].text_content().strip().split('\r') ) > 1:

        direccion_a = links[0].text_content().strip().split('\r')[0].strip()
        direccion_b = links[0].text_content().strip().split('\r')[1].strip()

        direccion = direccion_a + "\n" + direccion_b

    else:

        direccion = links[0].text_content().strip()

    
    telefono = "".join(links[1].text_content().split())
    fax = "".join(links[2].text_content().split())
    
    if len(links[3].cssselect("a")[0].attrib['href'])> len('http://'):

        web = links[3].cssselect("a")[0].attrib['href']

    else:
    
        web = ""

    return direccion, telefono, fax, web
    

cleaner = Cleaner()
cleaner.kill_tags = ['strong']

for i in range(1,45):
    base_url = 'http://planetafan.com/cas/site/tiendas.asp?prov=0&loc=0&pag='+str(i)
    
    html = scraperwiki.scrape(base_url)
    root = lxml.html.fromstring(html)
    links = root.cssselect("ul#listado-productos li")
    
    for link in links:

        record = {}

        name = link.cssselect("a")[0].text_content()
        card_link = link.cssselect("a")[0].attrib['href']
        address = link.cssselect("p")[0].text_content()

        direccion, telefono, fax, web = scrape_card('http://planetafan.com/cas/site/'+card_link)
        
        #process

        address = address.replace('(','')
        address = address.replace(')','')
        address = address.replace('C/','Calle')
        address = address.replace('C\\','Calle')
        #address = address.replace('Pº','Paseo')
    
        print direccion, telefono, fax, web

        record['idx'] = idx
        record['name'] = name
        record['address'] = address
        record['address_display'] = direccion
        record['phone'] = telefono
        record['fax'] = fax
        record['web'] = web

        scraperwiki.sqlite.save(['idx'], record)

        idx = idx + 1
        
    time.sleep(1)
