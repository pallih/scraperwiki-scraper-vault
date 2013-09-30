import scraperwiki
import BeautifulSoup

# Blank Python

import sys
import lxml.html
from urllib import urlencode
import json
import re
from BeautifulSoup import BeautifulSoup
from lxml import etree
import string

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

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def everything_between(text,begin,end):
    idx1=text.find(begin)
    idx2=text.find(end,idx1)
    return text[idx1+len(begin):idx2].strip()


searchURL = "http://www.youinweb.it/profiles_it/20044/visim-srl_370421.htm"

html = scraperwiki.scrape(searchURL)
root = lxml.html.fromstring(html)
doc = lxml.html.document_fromstring(html)


for el in doc.find_class('sicdescription'):
    sicdescription= el.text

for el in doc.find_class('companynamenormal'):
    ditta = el.text

for el in doc.find_class('summary'):
    dittacompleto  = el.text

for el in doc.find_class('phone'):
    telefono = el.text

i = 1
indirizzo = []
for el in doc.find_class('address'):
    indirizzo.append (el.text)
    i = i + 1

for el in doc.find_class('latlong'):
    print "GPS " + (el.text)
    i = i + 1


print "Ditta " + ditta
print "DittaCompleto " + dittacompleto
print "Telefono " + telefono
print "Indirizzo Via " + indirizzo[0]
print "Indirizzo Citta " + indirizzo[1]
print "Indirizzo Nazione " + indirizzo[2]
print "Descrizione " + sicdescription
    
cities = []
for el in doc.find_class('cityzip'):
    #print "Tag : " + str(el.tag)
    print "Tag : " + str(el.text)
    print "Tag : " + str(el.get('href'))
    cities.append (el.text)

sicnotes = []
for el in doc.find_class('SICnote'):
    #print "Tag : " + str(el.tag)
    print "Tag : " + str(el.text)
    print "Tag : " + str(el.get('href'))
    sicnotes.append (el.text)

for el in doc.find_class('keyword'):
    #print "Tag : " + str(el.tag)
    print "Tag : " + str(el.get('href'))

i = 0
for el in root.cssselect("div.samebusinessbox a"):
    print el.text
    print el.get('href') + " " + cities[i]
    i = i + 1

for el in root.cssselect("div.localbusinessbox a"):
    print el.text
    print el.get('href')
import scraperwiki
import BeautifulSoup

# Blank Python

import sys
import lxml.html
from urllib import urlencode
import json
import re
from BeautifulSoup import BeautifulSoup
from lxml import etree
import string

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

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def everything_between(text,begin,end):
    idx1=text.find(begin)
    idx2=text.find(end,idx1)
    return text[idx1+len(begin):idx2].strip()


searchURL = "http://www.youinweb.it/profiles_it/20044/visim-srl_370421.htm"

html = scraperwiki.scrape(searchURL)
root = lxml.html.fromstring(html)
doc = lxml.html.document_fromstring(html)


for el in doc.find_class('sicdescription'):
    sicdescription= el.text

for el in doc.find_class('companynamenormal'):
    ditta = el.text

for el in doc.find_class('summary'):
    dittacompleto  = el.text

for el in doc.find_class('phone'):
    telefono = el.text

i = 1
indirizzo = []
for el in doc.find_class('address'):
    indirizzo.append (el.text)
    i = i + 1

for el in doc.find_class('latlong'):
    print "GPS " + (el.text)
    i = i + 1


print "Ditta " + ditta
print "DittaCompleto " + dittacompleto
print "Telefono " + telefono
print "Indirizzo Via " + indirizzo[0]
print "Indirizzo Citta " + indirizzo[1]
print "Indirizzo Nazione " + indirizzo[2]
print "Descrizione " + sicdescription
    
cities = []
for el in doc.find_class('cityzip'):
    #print "Tag : " + str(el.tag)
    print "Tag : " + str(el.text)
    print "Tag : " + str(el.get('href'))
    cities.append (el.text)

sicnotes = []
for el in doc.find_class('SICnote'):
    #print "Tag : " + str(el.tag)
    print "Tag : " + str(el.text)
    print "Tag : " + str(el.get('href'))
    sicnotes.append (el.text)

for el in doc.find_class('keyword'):
    #print "Tag : " + str(el.tag)
    print "Tag : " + str(el.get('href'))

i = 0
for el in root.cssselect("div.samebusinessbox a"):
    print el.text
    print el.get('href') + " " + cities[i]
    i = i + 1

for el in root.cssselect("div.localbusinessbox a"):
    print el.text
    print el.get('href')
