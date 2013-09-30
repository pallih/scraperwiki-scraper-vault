# Shopping Centers in Portugal

import scraperwiki
import urlparse
import lxml.html

from BeautifulSoup import BeautifulSoup

from lxml import etree

base_url = 'http://www.apcc.pt/centros/centro.aspx?id='

max_id=200


#print soup

# GET SHOPPING NAME

def getshoppingname(base_soup):
    retval=0
    table_assoc=base_soup.find('table',{ 'class' : 'fichaAssocContentTable'})
    if table_assoc is not None:
        shopping=table_assoc.find('div', { 'class' : 'txtTitleRed'}).text
        retval=shopping
    return retval
  
# GET ATTRIBUTES
def getshoppingattribs(base_soup):
    info = {}
    i=0
    mastertable=base_soup.find('table',{ 'class' : 'fichaAssocContentTable' })
    #print table.tr.td.text
    records = [] # store all of the records in this list
    for table in mastertable.findAll('table'):
        for row in table.findAll('tr'):
            col = row.findAll('td')
            atributo = col[0].text
            valor = col[1].text
            record = '%s;%s' % (atributo, valor) 
            records.append(record)
            info[i]=valor
            i=i+1
    return info

def scrapeshopping(id):
    url=base_url + str(id)
    print id
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    shopping_name=getshoppingname(soup)
    if shopping_name is not 0:
        info=getshoppingattribs(soup)
        storeinfo(id,info,shopping_name)
    return soup

def storeinfo(id_s,info,name_s):
    print id_s
    print name_s
    print info
    data1={"id":id_s,"name":name_s,"contacto":info[0],"promotor":info[1],"gestor":info[2],"propriedade":info[3],"gestor":info[4],"abl":info[4],"nlojas":info[5],"morada":info[6],"cp7":info[7],"telefone":info[8],"website":info[11]}
    scraperwiki.sqlite.save(unique_keys=["id", "name"], data=data1)


def scrapeAllShoppings():
    for i in range(max_id):
        scrapeshopping(i+1)

#scrapeshopping(84)
scrapeAllShoppings()
print scraperwiki.sqlite.select("* from swdata")
# Shopping Centers in Portugal

import scraperwiki
import urlparse
import lxml.html

from BeautifulSoup import BeautifulSoup

from lxml import etree

base_url = 'http://www.apcc.pt/centros/centro.aspx?id='

max_id=200


#print soup

# GET SHOPPING NAME

def getshoppingname(base_soup):
    retval=0
    table_assoc=base_soup.find('table',{ 'class' : 'fichaAssocContentTable'})
    if table_assoc is not None:
        shopping=table_assoc.find('div', { 'class' : 'txtTitleRed'}).text
        retval=shopping
    return retval
  
# GET ATTRIBUTES
def getshoppingattribs(base_soup):
    info = {}
    i=0
    mastertable=base_soup.find('table',{ 'class' : 'fichaAssocContentTable' })
    #print table.tr.td.text
    records = [] # store all of the records in this list
    for table in mastertable.findAll('table'):
        for row in table.findAll('tr'):
            col = row.findAll('td')
            atributo = col[0].text
            valor = col[1].text
            record = '%s;%s' % (atributo, valor) 
            records.append(record)
            info[i]=valor
            i=i+1
    return info

def scrapeshopping(id):
    url=base_url + str(id)
    print id
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    shopping_name=getshoppingname(soup)
    if shopping_name is not 0:
        info=getshoppingattribs(soup)
        storeinfo(id,info,shopping_name)
    return soup

def storeinfo(id_s,info,name_s):
    print id_s
    print name_s
    print info
    data1={"id":id_s,"name":name_s,"contacto":info[0],"promotor":info[1],"gestor":info[2],"propriedade":info[3],"gestor":info[4],"abl":info[4],"nlojas":info[5],"morada":info[6],"cp7":info[7],"telefone":info[8],"website":info[11]}
    scraperwiki.sqlite.save(unique_keys=["id", "name"], data=data1)


def scrapeAllShoppings():
    for i in range(max_id):
        scrapeshopping(i+1)

#scrapeshopping(84)
scrapeAllShoppings()
print scraperwiki.sqlite.select("* from swdata")
