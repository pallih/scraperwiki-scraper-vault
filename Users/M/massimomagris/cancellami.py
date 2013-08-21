import scraperwiki
import sys
import lxml.html
from urllib import urlencode
import json
import re
import BeautifulSoup
from lxml import etree
import string
import mechanize
from BeautifulSoup import BeautifulSoup

# Genera elenco 

def salta(txt):
    return '\r'.join([x for x in txt.split("\r") if x.strip()!=''])

def cerca(html,search,nrline,offset):
    i=html.find(search)
    if i > 0:
        i=i+len(search)
        j=i+offset
        #esegue split ed elimina tutto quello che inizia con <
        s = html[i:j]
        s = s.splitlines(nrline)
        return (s[nrline])
    else:
        return ''


def estrai(html,search,nrline,offset):
    i=html.find(search)
    if i > 0:
        i=i+len(search)
        j=i+offset
        s = html[i:j]
        return (s)
    else:
        return ''

def everything_between(text,begin,end):
    idx1=text.find(begin)
    idx2=text.find(end,idx1)
    return text[idx1+len(begin):idx2].strip()

def split_line(text):

    # split the text
    words = text.split("\r")

    # for each word in the line:
    i = 0
    for word in words:

        # prints each word on a line
        print"I : " + str(i)+ "LEN " + str (len (word)) + " WORD : " + (word)
        print ord (word[1])
        i = i + 1

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

def using_in(text, stopwords):
#"return 1 (true) if any of the stopwords are in text -- using in"
    for word in stopwords:
        if word in text:
            return 1
    return 0

def salva (ragione,pagine,offset):
    
    url = sURL.replace ("RAGIONE",ragione)

    br.open(url)
    
    pagine = range(offset+2,pagine) 
    
    stopSet = set(["Logo", "Guarda il", "Invia", "Localizzare","Web Link","Localizzate","Link of","[IMG]","Visualizza"])
    
    i = 0
    i = offset * 20

    for p in pagine:
        print "Pagine " + str(p)

        searchURL= sURL2.replace ("PAGINA",str(p))
        searchURL= searchURL.replace ("OFFSET",str(i))
        response = br.open(searchURL)
        html = response.read()
    
        for link in br.links():
    
            if using_in (link.text,stopSet) <=0 and len (link.text) > 3:
              
                if str(link).find ("linkComp"):
                    try:
                        if link.title:print link.title
                    except Exception, err:
                        pass
            
                    a = link.attrs
                    if str(a).find ("linkComp") > 0:
                        if len(a[1]) > 0:
                            Nome = str(link.text)
                            URL=str(a[1][1])
                            # print Nome + " URL : " + URL
                            li = {}
                            li['Nome'] = Nome
                            li['URL'] = URL
                            scraperwiki.sqlite.save(unique_keys=['URL'], data=li)
        i = i + 20
    return

#INIZIO
sURL = "http://it.kompass.com/MarketingViewWeb/appmanager/kim/ITA_Portal?mktInfo_BasicSearchPortlet_1isMainSearch=true"
sURL = sURL + "&_nfpb=true&_windowLabel=mktInfo_BasicSearchPortlet_1&mktInfo_BasicSearchPortlet_1_actionOverride=%252Fflows%252"
sURL = sURL + "FmarketingInformation%252FbasicSearch%252FlaunchSearch&_pageLabel=common_homePage&mktInfo_BasicSearchPortlet_1%7"
sURL = sURL + "BactionForm.userLanguage%7D=it&mktInfo_BasicSearchPortlet_1%7BactionForm.userParameterSearch%7D=RAGIONE&"
sURL = sURL + "mktInfo_BasicSearchPortlet_1wlw-select_key%3A%7BactionForm.typeSearch%7DOldValue=true&"
sURL = sURL + "mktInfo_BasicSearchPortlet_1wlw-select_key%3A%7BactionForm.typeSearch%7D=CN&"
sURL = sURL + "mktInfo_BasicSearchPortlet_1wlw-select_key%3A%7BactionForm.geoSearch%7DOldValue=true&"
sURL = sURL + "mktInfo_BasicSearchPortlet_1wlw-select_key%3A%7BactionForm.geoSearch%7D=ITA"

#SEGUITO
sURL2 = "http://it.kompass.com/MarketingViewWeb/appmanager/kim/ITA_Portal?_nfpb=true&_windowLabel="
sURL2 = sURL2 + "mktInfo_EstablishmentListPortlet&mktInfo_EstablishmentListPortlet_actionOverride=%2Fflows%2"
sURL2 = sURL2 + "FmarketingInformation%2Fresult%2FintermediateToResult&mktInfo_EstablishmentListPortletpage=PAGINA&"
sURL2 = sURL2 + "mktInfo_EstablishmentListPortletgeoScopePage=ITA-COUNTRY&mktInfo_EstablishmentListPortletoffset=OFFSET&_pageLabel="
sURL2 = sURL2 + "marketingInformation_establishmentResultsListPage"

br = mechanize.Browser()

#salva ("snc",1216,0) #Indice pagine andrebbe ricavato automaticamente
#salva ("srl",7816,0)
salva ("spa",1500,38)
#salva ("srl",7816,5000)


#Recuperare la descrizione di sintesi
#Aggiungere SNC e altre forme
#<div class="floatLeft margeLeft10px width505px">
#                                    <span class="floatLeft">
#                                        <div class="width335px">
    
                                            
#                                                <span class="floatLeft">
#                                                    La GENNARO s.a.s. opera nel distretto delle Riparazioni Navali del Porto di Genova da oltre 70 anni con l'obiettivo #di servire il mondo dello shipping in maniera puntuale, affidabi...
#                                                </span>
#                                            
#    
#                                            
#    
#                                            
#                                        </div>
#                                    </span>

