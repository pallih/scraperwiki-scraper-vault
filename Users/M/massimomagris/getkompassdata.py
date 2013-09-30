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
        rs = s[nrline]
        rs = rs.strip ("\r")
        rs = rs.strip ("\n")
        return (rs)
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

sURL = "http://it.kompass.com/MarketingViewWeb/appmanager/kim/ITA_Portal?T400614181316703001758isMainSearch="
sURL = sURL + "true&_nfpb=true&_windowLabel=T400614181316703001758&T400614181316703001758_actionOverride=%252Fflows%252"
sURL = sURL + "FmarketingInformation%252FbasicSearch%252FlaunchSearch&_pageLabel=marketingInformation_establishmentResultsListPage"
sURL = sURL + "&T400614181316703001758%7BactionForm.userLanguage%7D=it&T400614181316703001758%7BactionForm.userParameterSearch%7D="
sURL = sURL + "FORMA&T400614181316703001758wlw-select_key%3A%7BactionForm.typeSearch%7"
sURL = sURL + "DOldValue=true&T400614181316703001758wlw-select_key%3A%7BactionForm.typeSearch%7D=CN&T400614181316703001758wlw-"
sURL = sURL + "select_key%3A%7BactionForm.geoSearch%7DOldValue=true&T400614181316703001758wlw-select_key%3A%7BactionForm.geoSearch%7D=ITA"
sURL = sURL + "&mktInfo_EstablishmentListPortletpage=PAGINA"

sURL = sURL.replace ("FORMA","spa")

sURL1 = "http://it.kompass.com/MarketingViewWeb/appmanager/kim/ITA_Portal?"
sURL1 = sURL1 + "_nfpb=true&_windowLabel=mktInfo_EstablishmentListPortlet&mktInfo_EstablishmentListPortlet_actionOverride=%2Fflows%2FmarketingInformation%"
sURL1 = sURL1 + "2Fresult%2FintermediateToResult&mktInfo_EstablishmentListPortletpage=PAGINA&"
sURL1 = sURL1 + "mktInfo_EstablishmentListPortletgeoScopePage=ITA-COUNTRY&mktInfo_EstablishmentListPortletoffset=260"
sURL1 = sURL1 + "&_pageLabel=marketingInformation_establishmentResultsListPage"

pagine = range(2,10)
searchURL= sURL.replace ("PAGINA","1")

searchURL = "http://it.kompass.com/profile_IT0091681_it/pietro-rosa-t.b.m.,-srl-gi.html"
searchURL = "http://it.kompass.com/profile_IT0013361_it/lima-lto,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0007795_it/malvestiti-ernesto,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0013361_it/lima-lto,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0047694_it/brovedani,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0180903_it/tech-value,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0007795_it/malvestiti-ernesto,-spa-gi.html"


#scraperwiki.sqlite.attach("listdatakd")
#data = scraperwiki.sqlite.select ('URL from ListDataKD.swdata')
data= scraperwiki.scrape("http://www.ammcomputer.com/temp/Mancanti.txt")
data = data.splitlines()


br = mechanize.Browser()
#print data


#scraperwiki.metadata.save('data_columns', ['Nome', 'Indirizzo', 'Citta', 'Nazione', 'Tel', 'Fax', 'PartitaIva', 'Codicefiscale', 'NumeroDipendenti', 'Codicefiscale','IDKompass ', 'FormaGiuridica', 'Fatturato', 'RegistrationNumber','URL'])

#print "<table>"           
#print "<tr><th>url</th><th>Nome</th>"
for d in data:
    try:
#        URL = d["URL"].replace ("-ps.html","-gi.html")
        URL = d.replace ("-ps.html","-gi.html")

        #sql = 'select count (*) from swdata where URL = "' + URL + '"'
        #res = scraperwiki.sqlite.execute(sql)
        #sql = 'count (*) from swdata where URL = "' + URL + '"'
        #res = scraperwiki.sqlite.select(sql)
        #f = str(res['data'][0])
        if 2>0:

            print URL
            #html = scraperwiki.scrape(d["URL"])
            #html = scraperwiki.scrape(sURLspa)
            #html = scraperwiki.scrape(sURLsrl)
        
            #br.open(URL)
            response = br.open(URL)
            html = response.read()
            print URL
            #html = scraperwiki.scrape(d["URL"])
            #html = scraperwiki.scrape(sURLspa)
            #html = scraperwiki.scrape(sURLsrl)
        
            #br.open(URL)
            response = br.open(URL)
            html = response.read()
        
            #root = lxml.html.fromstring(html)
                                
            html = salta(html)
            html = html.replace("\n",'')
            html = html.replace("\t",'')
            html = html.replace("&nbsp;",'')
          
    
            #DataFondazione=everything_between (cerca (html,'Data di fondazione',3,100),'\">','<') 
            #print DataFondazione
            
            if html.find ("ID Kompass") > 0:
                IDKompass = cerca (html,'ID Kompass',3,200)
                FormaGiuridica = everything_between (cerca (html,'Forma giuridica',1,200),'">','<')
                Fatturato = cerca (html,'Fatturato',3,200)
                PartitaIva = cerca (html,'Partita IVA',3,200)
                RegistrationNumber = cerca (html,'Registration number',3,200)
                Codicefiscale = cerca (html,'Codice Fiscale',3,200)
                CapitaleAzionarioEmesso =cerca (html,'Capitale azionario emesso',3,200)
                NumeroDipendenti =cerca (html,'Numero di dipendenti',1,200)[28:]
                Telefono = cerca(html,'Tel:',0,200)
                Fax = cerca (html,'Fax:',0,200)
                SitoInternet = everything_between (cerca (html,'Passa a http',0,200),"://"," (n")
            else:
                IDKompass = cerca (html,'ID Kompass',3,200)
                FormaGiuridica = cerca (html,'Forma giuridica',1,200)
                Fatturato = cerca (html,'Fatturato',1,200)
                PartitaIva = cerca (html,'Partita IVA',1,200)
                RegistrationNumber = cerca (html,'Registration number',1,200)
                Codicefiscale = cerca (html,'Codice Fiscale',1,200)
                CapitaleAzionarioEmesso =cerca (html,'Capitale azionario emesso',1,200)
                NumeroDipendenti =cerca (html,'Numero di dipendenti',1,200)
                Telefono = cerca(html,'Tel:',0,200)
                Fax = cerca (html,'Fax:',0,200)
            
            descrcomp = estrai(html,'description_company',1,800).replace ('<br/>','')
            descrcomp = descrcomp .replace ('</br>','')
            
            linee = descrcomp.split("\r")
            
            Nome = everything_between (linee [1],'">','</')
            Indirizzo0 = linee [3]
            Indirizzo1 =  linee [4]
            Indirizzo2 =  linee [5]
            li = {}
            
            li['Nome'] = Nome
            li['Indirizzo'] = Indirizzo0
            li['Citta'] = Indirizzo1
            li['Nazione'] = Indirizzo2
            li['Tel'] = Telefono
            li['Fax'] = Fax
            li['IDKompass '] = IDKompass 
            li['FormaGiuridica'] = FormaGiuridica
            li['Fatturato'] = Fatturato
            li['RegistrationNumber'] = RegistrationNumber 
            li['PartitaIva'] = PartitaIva
            li['Codicefiscale'] = Codicefiscale
            CapitaleAzionarioEmesso = CapitaleAzionarioEmesso.replace ("<label>","")
            CapitaleAzionarioEmesso = CapitaleAzionarioEmesso.replace ("</label>","")
            li['CapitaleAzionarioEmesso'] =  CapitaleAzionarioEmesso 
            li['NumeroDipendenti'] = NumeroDipendenti
            li['URL'] = URL
            scraperwiki.sqlite.save(unique_keys=['PartitaIva'], data=li)
        else:
            print "skip " + URL
    except Exception, err:
        print ('ERROR: %s\n' % str(err))

#    print "Nome: " + Nome
#    print "Via : " + Indirizzo0
#    print "Citta  : " + Indirizzo1
#    print "Paese  : " + Indirizzo2
#    print "Telefono : " + Telefono
#    print "Fax : " + Fax
    
#    print "ID Kompass : " + IDKompass 
#    print "FormaGiuridica  : " + FormaGiuridica 
#    print "Fatturato  : " + Fatturato 
#    print "PartitaIva   : " + PartitaIva 
#    print "RegistrationNumber  : " + RegistrationNumber 
#    print "Codicefiscale : " + Codicefiscale 
#    print "CapitaleAzionarioEmesso : " + CapitaleAzionarioEmesso 
#    print "NumeroDipendenti : " + NumeroDipendenti 
    

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
        rs = s[nrline]
        rs = rs.strip ("\r")
        rs = rs.strip ("\n")
        return (rs)
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

sURL = "http://it.kompass.com/MarketingViewWeb/appmanager/kim/ITA_Portal?T400614181316703001758isMainSearch="
sURL = sURL + "true&_nfpb=true&_windowLabel=T400614181316703001758&T400614181316703001758_actionOverride=%252Fflows%252"
sURL = sURL + "FmarketingInformation%252FbasicSearch%252FlaunchSearch&_pageLabel=marketingInformation_establishmentResultsListPage"
sURL = sURL + "&T400614181316703001758%7BactionForm.userLanguage%7D=it&T400614181316703001758%7BactionForm.userParameterSearch%7D="
sURL = sURL + "FORMA&T400614181316703001758wlw-select_key%3A%7BactionForm.typeSearch%7"
sURL = sURL + "DOldValue=true&T400614181316703001758wlw-select_key%3A%7BactionForm.typeSearch%7D=CN&T400614181316703001758wlw-"
sURL = sURL + "select_key%3A%7BactionForm.geoSearch%7DOldValue=true&T400614181316703001758wlw-select_key%3A%7BactionForm.geoSearch%7D=ITA"
sURL = sURL + "&mktInfo_EstablishmentListPortletpage=PAGINA"

sURL = sURL.replace ("FORMA","spa")

sURL1 = "http://it.kompass.com/MarketingViewWeb/appmanager/kim/ITA_Portal?"
sURL1 = sURL1 + "_nfpb=true&_windowLabel=mktInfo_EstablishmentListPortlet&mktInfo_EstablishmentListPortlet_actionOverride=%2Fflows%2FmarketingInformation%"
sURL1 = sURL1 + "2Fresult%2FintermediateToResult&mktInfo_EstablishmentListPortletpage=PAGINA&"
sURL1 = sURL1 + "mktInfo_EstablishmentListPortletgeoScopePage=ITA-COUNTRY&mktInfo_EstablishmentListPortletoffset=260"
sURL1 = sURL1 + "&_pageLabel=marketingInformation_establishmentResultsListPage"

pagine = range(2,10)
searchURL= sURL.replace ("PAGINA","1")

searchURL = "http://it.kompass.com/profile_IT0091681_it/pietro-rosa-t.b.m.,-srl-gi.html"
searchURL = "http://it.kompass.com/profile_IT0013361_it/lima-lto,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0007795_it/malvestiti-ernesto,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0013361_it/lima-lto,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0047694_it/brovedani,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0180903_it/tech-value,-spa-gi.html"
searchURL = "http://it.kompass.com/profile_IT0007795_it/malvestiti-ernesto,-spa-gi.html"


#scraperwiki.sqlite.attach("listdatakd")
#data = scraperwiki.sqlite.select ('URL from ListDataKD.swdata')
data= scraperwiki.scrape("http://www.ammcomputer.com/temp/Mancanti.txt")
data = data.splitlines()


br = mechanize.Browser()
#print data


#scraperwiki.metadata.save('data_columns', ['Nome', 'Indirizzo', 'Citta', 'Nazione', 'Tel', 'Fax', 'PartitaIva', 'Codicefiscale', 'NumeroDipendenti', 'Codicefiscale','IDKompass ', 'FormaGiuridica', 'Fatturato', 'RegistrationNumber','URL'])

#print "<table>"           
#print "<tr><th>url</th><th>Nome</th>"
for d in data:
    try:
#        URL = d["URL"].replace ("-ps.html","-gi.html")
        URL = d.replace ("-ps.html","-gi.html")

        #sql = 'select count (*) from swdata where URL = "' + URL + '"'
        #res = scraperwiki.sqlite.execute(sql)
        #sql = 'count (*) from swdata where URL = "' + URL + '"'
        #res = scraperwiki.sqlite.select(sql)
        #f = str(res['data'][0])
        if 2>0:

            print URL
            #html = scraperwiki.scrape(d["URL"])
            #html = scraperwiki.scrape(sURLspa)
            #html = scraperwiki.scrape(sURLsrl)
        
            #br.open(URL)
            response = br.open(URL)
            html = response.read()
            print URL
            #html = scraperwiki.scrape(d["URL"])
            #html = scraperwiki.scrape(sURLspa)
            #html = scraperwiki.scrape(sURLsrl)
        
            #br.open(URL)
            response = br.open(URL)
            html = response.read()
        
            #root = lxml.html.fromstring(html)
                                
            html = salta(html)
            html = html.replace("\n",'')
            html = html.replace("\t",'')
            html = html.replace("&nbsp;",'')
          
    
            #DataFondazione=everything_between (cerca (html,'Data di fondazione',3,100),'\">','<') 
            #print DataFondazione
            
            if html.find ("ID Kompass") > 0:
                IDKompass = cerca (html,'ID Kompass',3,200)
                FormaGiuridica = everything_between (cerca (html,'Forma giuridica',1,200),'">','<')
                Fatturato = cerca (html,'Fatturato',3,200)
                PartitaIva = cerca (html,'Partita IVA',3,200)
                RegistrationNumber = cerca (html,'Registration number',3,200)
                Codicefiscale = cerca (html,'Codice Fiscale',3,200)
                CapitaleAzionarioEmesso =cerca (html,'Capitale azionario emesso',3,200)
                NumeroDipendenti =cerca (html,'Numero di dipendenti',1,200)[28:]
                Telefono = cerca(html,'Tel:',0,200)
                Fax = cerca (html,'Fax:',0,200)
                SitoInternet = everything_between (cerca (html,'Passa a http',0,200),"://"," (n")
            else:
                IDKompass = cerca (html,'ID Kompass',3,200)
                FormaGiuridica = cerca (html,'Forma giuridica',1,200)
                Fatturato = cerca (html,'Fatturato',1,200)
                PartitaIva = cerca (html,'Partita IVA',1,200)
                RegistrationNumber = cerca (html,'Registration number',1,200)
                Codicefiscale = cerca (html,'Codice Fiscale',1,200)
                CapitaleAzionarioEmesso =cerca (html,'Capitale azionario emesso',1,200)
                NumeroDipendenti =cerca (html,'Numero di dipendenti',1,200)
                Telefono = cerca(html,'Tel:',0,200)
                Fax = cerca (html,'Fax:',0,200)
            
            descrcomp = estrai(html,'description_company',1,800).replace ('<br/>','')
            descrcomp = descrcomp .replace ('</br>','')
            
            linee = descrcomp.split("\r")
            
            Nome = everything_between (linee [1],'">','</')
            Indirizzo0 = linee [3]
            Indirizzo1 =  linee [4]
            Indirizzo2 =  linee [5]
            li = {}
            
            li['Nome'] = Nome
            li['Indirizzo'] = Indirizzo0
            li['Citta'] = Indirizzo1
            li['Nazione'] = Indirizzo2
            li['Tel'] = Telefono
            li['Fax'] = Fax
            li['IDKompass '] = IDKompass 
            li['FormaGiuridica'] = FormaGiuridica
            li['Fatturato'] = Fatturato
            li['RegistrationNumber'] = RegistrationNumber 
            li['PartitaIva'] = PartitaIva
            li['Codicefiscale'] = Codicefiscale
            CapitaleAzionarioEmesso = CapitaleAzionarioEmesso.replace ("<label>","")
            CapitaleAzionarioEmesso = CapitaleAzionarioEmesso.replace ("</label>","")
            li['CapitaleAzionarioEmesso'] =  CapitaleAzionarioEmesso 
            li['NumeroDipendenti'] = NumeroDipendenti
            li['URL'] = URL
            scraperwiki.sqlite.save(unique_keys=['PartitaIva'], data=li)
        else:
            print "skip " + URL
    except Exception, err:
        print ('ERROR: %s\n' % str(err))

#    print "Nome: " + Nome
#    print "Via : " + Indirizzo0
#    print "Citta  : " + Indirizzo1
#    print "Paese  : " + Indirizzo2
#    print "Telefono : " + Telefono
#    print "Fax : " + Fax
    
#    print "ID Kompass : " + IDKompass 
#    print "FormaGiuridica  : " + FormaGiuridica 
#    print "Fatturato  : " + Fatturato 
#    print "PartitaIva   : " + PartitaIva 
#    print "RegistrationNumber  : " + RegistrationNumber 
#    print "Codicefiscale : " + Codicefiscale 
#    print "CapitaleAzionarioEmesso : " + CapitaleAzionarioEmesso 
#    print "NumeroDipendenti : " + NumeroDipendenti 
    

