#Esempio recupero elenco aziende

import scraperwiki
import array
import lxml.html
from urllib import urlencode
import json
import re

# Tutorial Data Extraction

def get_text(el, class_name):
    els = el.find_class(class_name)
    if els:
        return els[0].text_content()
    else:
        return ''

def get_href(el, class_name):
    els = el.find_class(class_name)
    if els:
        return els[0].get('href')
    else:
        return ''

def get_value(el):
    return get_text(el, 'value') or el.text_content()

def get_all_texts(el, class_name):
    return [e.text_content() for e in els.find_class(class_name)]

def parse_addresses(el):
    return el.find_class('adr')

for el in range(359) : 
    print el+1
    urlRoot = ''.join(('http://www.paginegialle.it/pgol/4-concessionarie%20auto/p-', str(el+1), '?mr=50'))   
    html = scraperwiki.scrape(urlRoot)
    print html
    root = lxml.html.fromstring(html)

    li = {}

    companies = []
    name = []
    url = []
    address = []
    locality = []
    website = []
    tel = []
    email = []
    category = []


    for el in root.xpath("//a[@class='_lms _noc']/@href"):url.append(el)

    for el in root.cssselect("div.org"):
        name.append (get_text (el,"rgs"))

    for el in root.cssselect("div.address"):
        address.append (get_text (el,"street-address"))

    for el in root.cssselect("div.address"):
        locality.append (get_text (el,"locality"))

    for el in root.cssselect("div.tel"):
        tel.append (get_text (el,"tel") )

    for el in root.cssselect("div.link"):
        website.append (get_href (el,"_noc") )  

    for el in root.cssselect("div.text"):
        category.append (get_text (el,"snippet") )  

    i = 0
    for el in root.cssselect("div.org"):
        k = 1
        print 'Name ', name[i]
        print 'Address ', address[i]
        print 'Locality ', locality[i]
        print 'Tel', tel[i]    
        print 'Website', website[i]
        print 'Category', category[i]
        htmlDetails =  scraperwiki.scrape(url[i])
        rootDetail = lxml.html.fromstring(htmlDetails)
        for el in rootDetail.xpath("//input[@name='multimail']/@value"):li['Email'] = el
        urlemail = ''.join(( url[i], '/contatto?lt=frag'))
        print urlemail                
        try:
            htmlEmail =  scraperwiki.scrape(urlemail)
        except:                 
               k = 0
               print 'Error caught'
        if k == 1: 
                  print htmlEmail
                  rootEmail = lxml.html.fromstring(htmlEmail)
                  for el in rootEmail.xpath("//input[@name='multimail']/@value"):li['Email'] = el 
        if k == 0:
                  li['Email'] = ""       
        li['CompanyName'] = name[i].upper().replace("\n","")
        li['Address'] = address[i].upper().replace("\n","")
        li['Locality'] = locality[i].upper().replace("\n","")
        li['Tel'] = tel[i].upper().replace("\n","")
        li['WebSite'] = website[i].lower().replace("\n","")
        li['Category'] = category[i].upper().replace("\n","") 
        scraperwiki.sqlite.save(unique_keys=['CompanyName'], data=li)
        i = i + 1

#Fine Recupero elenco aziende
#Esempio recupero elenco aziende

import scraperwiki
import array
import lxml.html
from urllib import urlencode
import json
import re

# Tutorial Data Extraction

def get_text(el, class_name):
    els = el.find_class(class_name)
    if els:
        return els[0].text_content()
    else:
        return ''

def get_href(el, class_name):
    els = el.find_class(class_name)
    if els:
        return els[0].get('href')
    else:
        return ''

def get_value(el):
    return get_text(el, 'value') or el.text_content()

def get_all_texts(el, class_name):
    return [e.text_content() for e in els.find_class(class_name)]

def parse_addresses(el):
    return el.find_class('adr')

for el in range(359) : 
    print el+1
    urlRoot = ''.join(('http://www.paginegialle.it/pgol/4-concessionarie%20auto/p-', str(el+1), '?mr=50'))   
    html = scraperwiki.scrape(urlRoot)
    print html
    root = lxml.html.fromstring(html)

    li = {}

    companies = []
    name = []
    url = []
    address = []
    locality = []
    website = []
    tel = []
    email = []
    category = []


    for el in root.xpath("//a[@class='_lms _noc']/@href"):url.append(el)

    for el in root.cssselect("div.org"):
        name.append (get_text (el,"rgs"))

    for el in root.cssselect("div.address"):
        address.append (get_text (el,"street-address"))

    for el in root.cssselect("div.address"):
        locality.append (get_text (el,"locality"))

    for el in root.cssselect("div.tel"):
        tel.append (get_text (el,"tel") )

    for el in root.cssselect("div.link"):
        website.append (get_href (el,"_noc") )  

    for el in root.cssselect("div.text"):
        category.append (get_text (el,"snippet") )  

    i = 0
    for el in root.cssselect("div.org"):
        k = 1
        print 'Name ', name[i]
        print 'Address ', address[i]
        print 'Locality ', locality[i]
        print 'Tel', tel[i]    
        print 'Website', website[i]
        print 'Category', category[i]
        htmlDetails =  scraperwiki.scrape(url[i])
        rootDetail = lxml.html.fromstring(htmlDetails)
        for el in rootDetail.xpath("//input[@name='multimail']/@value"):li['Email'] = el
        urlemail = ''.join(( url[i], '/contatto?lt=frag'))
        print urlemail                
        try:
            htmlEmail =  scraperwiki.scrape(urlemail)
        except:                 
               k = 0
               print 'Error caught'
        if k == 1: 
                  print htmlEmail
                  rootEmail = lxml.html.fromstring(htmlEmail)
                  for el in rootEmail.xpath("//input[@name='multimail']/@value"):li['Email'] = el 
        if k == 0:
                  li['Email'] = ""       
        li['CompanyName'] = name[i].upper().replace("\n","")
        li['Address'] = address[i].upper().replace("\n","")
        li['Locality'] = locality[i].upper().replace("\n","")
        li['Tel'] = tel[i].upper().replace("\n","")
        li['WebSite'] = website[i].lower().replace("\n","")
        li['Category'] = category[i].upper().replace("\n","") 
        scraperwiki.sqlite.save(unique_keys=['CompanyName'], data=li)
        i = i + 1

#Fine Recupero elenco aziende
