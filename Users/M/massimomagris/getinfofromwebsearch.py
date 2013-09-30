import scraperwiki
import sys
import lxml.html
from urllib import urlencode
import json
import re
from BeautifulSoup import BeautifulSoup
from lxml import etree
import string

# cerca info
# Sito
# Email
# Piva
# dato il nome di un azienda

#es. union stampi srl info
#http://www.metacrawler.com/search/web?fcoid=417&fcop=topnav&fpid=2&q=union+stampi+srl+info&ql=



searchURL = "http://www.metacrawler.com/search/web?fcoid=417&fcop=topnav&fpid=2&q=union+stampi+srl+info&ql="
searchURL = "http://www.metacrawler.com/search/web?fcoid=417&fcop=topnav&fpid=2&q=%22tech-value+spa%22+iva&ql="

html = scraperwiki.scrape(searchURL)
root = lxml.html.fromstring(html)
doc = lxml.html.document_fromstring(html)


trovati = []

items=  re.findall('resultDescription.*', html)
#Prende i primi tre
for item in items:
    item = item.replace ("<strong>","").replace ("</strong>","")
    #print item
    matches = re.findall ("IVA.{15}",item)
#    matches = re.findall ("IVA.(\w+)",item)
    for match in matches :  
        print match.replace ("IVA","")

items=  re.findall('resultDescription.*', html)
#Prende i primi tre
for item in items:
    item = item.replace ("<strong>","").replace ("</strong>","")
    print item
    matches = re.findall ("([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})",item)
#    print matches.group(0)
    for match in matches :  
        print match



    

#    print item

i = 1
indirizzo = []
for el in doc.find_class('resultDescription'):
    print(el.text)
    i = i + 1

for el in doc.find_class('div.resultDescription'):
    print  el.text
import scraperwiki
import sys
import lxml.html
from urllib import urlencode
import json
import re
from BeautifulSoup import BeautifulSoup
from lxml import etree
import string

# cerca info
# Sito
# Email
# Piva
# dato il nome di un azienda

#es. union stampi srl info
#http://www.metacrawler.com/search/web?fcoid=417&fcop=topnav&fpid=2&q=union+stampi+srl+info&ql=



searchURL = "http://www.metacrawler.com/search/web?fcoid=417&fcop=topnav&fpid=2&q=union+stampi+srl+info&ql="
searchURL = "http://www.metacrawler.com/search/web?fcoid=417&fcop=topnav&fpid=2&q=%22tech-value+spa%22+iva&ql="

html = scraperwiki.scrape(searchURL)
root = lxml.html.fromstring(html)
doc = lxml.html.document_fromstring(html)


trovati = []

items=  re.findall('resultDescription.*', html)
#Prende i primi tre
for item in items:
    item = item.replace ("<strong>","").replace ("</strong>","")
    #print item
    matches = re.findall ("IVA.{15}",item)
#    matches = re.findall ("IVA.(\w+)",item)
    for match in matches :  
        print match.replace ("IVA","")

items=  re.findall('resultDescription.*', html)
#Prende i primi tre
for item in items:
    item = item.replace ("<strong>","").replace ("</strong>","")
    print item
    matches = re.findall ("([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})",item)
#    print matches.group(0)
    for match in matches :  
        print match



    

#    print item

i = 1
indirizzo = []
for el in doc.find_class('resultDescription'):
    print(el.text)
    i = i + 1

for el in doc.find_class('div.resultDescription'):
    print  el.text
