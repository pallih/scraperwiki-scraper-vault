import scraperwiki
#import urlparse
import lxml.html


def scrape_table(root):

    rows = root.cssselect("div.info")
    for row in rows:

        record = {}

        table_cells = row.cssselect("h1")


        #if table_cells: 
        record['municipio'] = table_cells[0].text
            
            #record['ID'] = 'BUE'+item
        print record, '------------'
            
        scraperwiki.sqlite.save(["ID"], record)



def scrape_page(url):

    html = scraperwiki.scrape(url)
    print html

    root = lxml.html.fromstring(html)

    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
#base_url1 = 'http://www.mininterior.gov.ar/municipios/masinfo.php?municipio=BUE'
#base_url2 = '&idName=municipios&idNameSubMenu=&idNameSubMenuDer=&idNameSubMenuDerNivel2=&idNameSubMenuDerPrincipal='



#municIDs=['001','002','003']



#for item in municIDs:

  #  print item

 #   next_link = base_url1+item+base_url1

#    scrape_page(next_link)
url='http://www.mininterior.gov.ar/municipios/masinfo.php?municipio=BUE001&idName=municipios&idNameSubMenu=&idNameSubMenuDer=&idNameSubMenuDerNivel2=&idNameSubMenuDerPrincipal='
import scraperwiki
#import urlparse
import lxml.html


def scrape_table(root):

    rows = root.cssselect("div.info")
    for row in rows:

        record = {}

        table_cells = row.cssselect("h1")


        #if table_cells: 
        record['municipio'] = table_cells[0].text
            
            #record['ID'] = 'BUE'+item
        print record, '------------'
            
        scraperwiki.sqlite.save(["ID"], record)



def scrape_page(url):

    html = scraperwiki.scrape(url)
    print html

    root = lxml.html.fromstring(html)

    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
#base_url1 = 'http://www.mininterior.gov.ar/municipios/masinfo.php?municipio=BUE'
#base_url2 = '&idName=municipios&idNameSubMenu=&idNameSubMenuDer=&idNameSubMenuDerNivel2=&idNameSubMenuDerPrincipal='



#municIDs=['001','002','003']



#for item in municIDs:

  #  print item

 #   next_link = base_url1+item+base_url1

#    scrape_page(next_link)
url='http://www.mininterior.gov.ar/municipios/masinfo.php?municipio=BUE001&idName=municipios&idNameSubMenu=&idNameSubMenuDer=&idNameSubMenuDerNivel2=&idNameSubMenuDerPrincipal='
