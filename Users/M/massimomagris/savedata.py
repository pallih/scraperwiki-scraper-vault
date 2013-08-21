import scraperwiki

# Blank Python

import scraperwiki
import BeautifulSoup

# Get YouInWebPageInfo

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


scraperwiki.sqlite.attach("elencoyouinweb")
data = scraperwiki.sqlite.select(           
    '''* from ElencoYouInWeb.swdata where substr (CAP,1,1) in ('5','6','7','8','9')
   '''
)


for d in data:
    try:
        html = scraperwiki.scrape(d["URL"])
        doc = lxml.html.fromstring(html)
    
        li = {}
          
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
        
        #print "Ditta " + ditta
        #print "DittaCompleto " + dittacompleto
        #print "Telefono " + telefono
        #print "Indirizzo Via " + indirizzo[0]
        #print "Indirizzo Citta " + indirizzo[1]
        #print "Indirizzo Nazione " + indirizzo[2]
        #print "Descrizione " + sicdescription
    
        li['ditta'] = ditta
        li['telefono'] = telefono
        li['indirizzo0'] = indirizzo[0]
        li['indirizzo1'] = indirizzo[1]
        li['indirizzo2'] = indirizzo[2]
        li['sic'] = sicdescription
        scraperwiki.sqlite.save(unique_keys=['ditta','indirizzo0'], data=li)
    except Exception, err:
        print ('ERROR: %s\n' % str(err))
        pass
    
