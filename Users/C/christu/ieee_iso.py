# http://www.iso.org/iso/searchstandardsajax.htm?isAjax=abcd&qt=ISO%2FIEC&published=on&withdrawn=&development=&deleted=&sort=rel&ajax_url=searchstandardsajax.htm&target_search=standards&page=4


import scraperwiki
import re
import urllib
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

page = 1
searchURL = 'http://www.iso.org/iso/searchstandardsajax.htm?isAjax=abcd&qt=ISO%2FIEC&published=on&withdrawn=&development=&deleted=&sort=rel&ajax_url=searchstandardsajax.htm&target_search=standards&page='

def scrape_site(page):
    # packe die Page in einen string und adde dann noch die seitenzahl, die unten im code hochgezählt wird
    html = scraperwiki.scrape(searchURL+str(page))
    # der String wird in in unicode convertiert
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    # hier soll die tabelle auf der page gefunden werden, welche die einzige auf der page ist
    table = html.find('table')
    # hier sollen alle links aus der tabelle gefunden werden die iso_catalogue... lauten und hinten wird die nr jeweils dazugepackt
    links = table.findAll('a', href=re.compile(r'iso_catalogue/catalogue_tc/catalogue_detail\.htm\?csnumber=*'))
  
    
# die schleife ist falsch
    for a in links:
        match = re.search(r'iso_catalogue/catalogue_tc/catalogue_detail\.htm\?csnumber=.*', a['href'], re.M | re.I)
        print match
        if match:
            url = urllib.unqoute(match.group(1))
            try:
                scrape_content(url)
            except:
                print 'error for URL'+url
        else:
            print 'no match for'+a['href']


# teste ich diesen Block einzeln, bringt er keine fehlermeldung, wie kann ich std ausdrucken? per print macht er das nicht
def scrape_content(url):
    print url
    std={'id':url}
    print std
    html=scraperwiki.scrape(url)

    html=BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    print html

    content=html.find('div', id="content")
    print content
    div=content.find('div', {'class':'col66 fond'})
    std['StandardNr']=div.find('h1').text
    std['title']=div.find('h4').text
    # abstract=div.find('div',{'class':'highlightWhite'}).find('h3')
    abstract=div.find('h3', text='Abstract')
    std['abstract']=abstract.findNextSiblings('p')[1].text
                                             

    scraperwiki.sqlite.save(unique_keys=['id'], data=std,table_name='standards_iso')


if scraperwiki.sqlite.get_var('page')==None:
    scraperwiki.sqlite.save_var('page',0)
page = scraperwiki.sqlite.get_var('page')

#hier habe ich am anfang auch keinen fehler bekommen, aber als ich links dazugefügt habe, bekam ich einen fehler
while page <= 245:
    scrape_site(page)
    scraperwiki.sqlite.save_var('page',page)
    page = page + 1    
# http://www.iso.org/iso/searchstandardsajax.htm?isAjax=abcd&qt=ISO%2FIEC&published=on&withdrawn=&development=&deleted=&sort=rel&ajax_url=searchstandardsajax.htm&target_search=standards&page=4


import scraperwiki
import re
import urllib
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

page = 1
searchURL = 'http://www.iso.org/iso/searchstandardsajax.htm?isAjax=abcd&qt=ISO%2FIEC&published=on&withdrawn=&development=&deleted=&sort=rel&ajax_url=searchstandardsajax.htm&target_search=standards&page='

def scrape_site(page):
    # packe die Page in einen string und adde dann noch die seitenzahl, die unten im code hochgezählt wird
    html = scraperwiki.scrape(searchURL+str(page))
    # der String wird in in unicode convertiert
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    # hier soll die tabelle auf der page gefunden werden, welche die einzige auf der page ist
    table = html.find('table')
    # hier sollen alle links aus der tabelle gefunden werden die iso_catalogue... lauten und hinten wird die nr jeweils dazugepackt
    links = table.findAll('a', href=re.compile(r'iso_catalogue/catalogue_tc/catalogue_detail\.htm\?csnumber=*'))
  
    
# die schleife ist falsch
    for a in links:
        match = re.search(r'iso_catalogue/catalogue_tc/catalogue_detail\.htm\?csnumber=.*', a['href'], re.M | re.I)
        print match
        if match:
            url = urllib.unqoute(match.group(1))
            try:
                scrape_content(url)
            except:
                print 'error for URL'+url
        else:
            print 'no match for'+a['href']


# teste ich diesen Block einzeln, bringt er keine fehlermeldung, wie kann ich std ausdrucken? per print macht er das nicht
def scrape_content(url):
    print url
    std={'id':url}
    print std
    html=scraperwiki.scrape(url)

    html=BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    print html

    content=html.find('div', id="content")
    print content
    div=content.find('div', {'class':'col66 fond'})
    std['StandardNr']=div.find('h1').text
    std['title']=div.find('h4').text
    # abstract=div.find('div',{'class':'highlightWhite'}).find('h3')
    abstract=div.find('h3', text='Abstract')
    std['abstract']=abstract.findNextSiblings('p')[1].text
                                             

    scraperwiki.sqlite.save(unique_keys=['id'], data=std,table_name='standards_iso')


if scraperwiki.sqlite.get_var('page')==None:
    scraperwiki.sqlite.save_var('page',0)
page = scraperwiki.sqlite.get_var('page')

#hier habe ich am anfang auch keinen fehler bekommen, aber als ich links dazugefügt habe, bekam ich einen fehler
while page <= 245:
    scrape_site(page)
    scraperwiki.sqlite.save_var('page',page)
    page = page + 1    
