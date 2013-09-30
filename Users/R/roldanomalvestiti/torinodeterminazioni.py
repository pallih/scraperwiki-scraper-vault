import scraperwiki
import mechanize
import lxml.html           
from dateutil.parser import *
from datetime import *
from dateutil.relativedelta import *
import commands
import os
import re

def getDateDeterminazione(page):
    "calcola data da url"
    # estrai es 2012_01_01-15.htm
    htmlfile = page[-17:]
    if htmlfile.startswith('2'):
        print(htmlfile)
        anno = htmlfile[:4]
        mese = htmlfile[5:]
        mese = mese[:2]
        giorno = htmlfile[11:]
        giorno = giorno[:2]
        print(anno)
        print(mese)
        print(giorno)
    else :
        htmlfile = page[-16:]
        print(htmlfile)
        anno = htmlfile[:4]
        mese = htmlfile[5:]
        mese = mese[:2]
        giorno = htmlfile[10:]
        giorno = giorno[:2]
        print(anno)
        print(mese)
        print(giorno)

    return datetime.strptime(anno + "-" + mese + "-" + giorno, '%Y-%m-%d')


def scrapeSinglePage(page): 
    "scarica determinazioni da signole pagine"
    html = scraperwiki.scrape(page)
    #print html
    
    now = parse(commands.getoutput("date"))
    today = now.date()
    NOW = datetime.now()

    dataDeterminazione = getDateDeterminazione(page)
    print(dataDeterminazione)
    if relativedelta(dataDeterminazione, NOW) > 0:
        dataDeterminazione = NOW

    root = lxml.html.fromstring(html )
    divs = root.cssselect("div[id='corpo']")
    for div in divs:
        print(div)
        for tr in div.cssselect("tr.riga"):
            #print(tr)        
            tds = tr.cssselect("td")
            #print(td.text)
            
            # estrae importo
            importoStr = ""
            importo = 0
            matchObj = re.match( r'.*EURO ([0-9\.,]*).*', tds[2].text_content(), re.M|re.I)
            if matchObj:
                print "matchObj.group(1) : ", matchObj.group(1)
                importoStr =  matchObj.group(1)
                if importoStr .endswith('.') or importoStr .endswith(',') :
                    importoStr = importoStr [:len(importoStr )-1]
                # trasfoma in numero
                if len(importoStr) > 2:
                    importoStr = importoStr .replace(".","")
                    importoStr = importoStr .replace(",",".")
                    importo = float(importoStr)
            else:
                print "No match!!"

            if len(tds)==3:
                data = {
                   'num' : tds[0].text_content(),
                   'codice' : tds[1].text_content(),
                   'importo' : importo ,
                   'anno' : int(tds[1].text_content()[:4]),
                   'descrizione' : tds[2].text_content(),
                   'DataSalvataggio' : dataDeterminazione.date(),
                   'DataUltimoUpdate' : NOW,
                   'url' : page
               }
                print data
                scraperwiki.sqlite.save(unique_keys=['codice'], data=data)

    return


baseUrl ="http://www.comune.torino.it/determinazioni/2012/"
htmlTot = scraperwiki.scrape(baseUrl)
rootTot = lxml.html.fromstring(htmlTot)
divsTot = rootTot.cssselect("div.riga")
for div in divsTot:
    links = div.cssselect('a')
    for link in links:
        url = link.get('href','')
        if url.startswith( '2012' ):
            print(url)
            scrapeSinglePage(baseUrl + url)




import scraperwiki
import mechanize
import lxml.html           
from dateutil.parser import *
from datetime import *
from dateutil.relativedelta import *
import commands
import os
import re

def getDateDeterminazione(page):
    "calcola data da url"
    # estrai es 2012_01_01-15.htm
    htmlfile = page[-17:]
    if htmlfile.startswith('2'):
        print(htmlfile)
        anno = htmlfile[:4]
        mese = htmlfile[5:]
        mese = mese[:2]
        giorno = htmlfile[11:]
        giorno = giorno[:2]
        print(anno)
        print(mese)
        print(giorno)
    else :
        htmlfile = page[-16:]
        print(htmlfile)
        anno = htmlfile[:4]
        mese = htmlfile[5:]
        mese = mese[:2]
        giorno = htmlfile[10:]
        giorno = giorno[:2]
        print(anno)
        print(mese)
        print(giorno)

    return datetime.strptime(anno + "-" + mese + "-" + giorno, '%Y-%m-%d')


def scrapeSinglePage(page): 
    "scarica determinazioni da signole pagine"
    html = scraperwiki.scrape(page)
    #print html
    
    now = parse(commands.getoutput("date"))
    today = now.date()
    NOW = datetime.now()

    dataDeterminazione = getDateDeterminazione(page)
    print(dataDeterminazione)
    if relativedelta(dataDeterminazione, NOW) > 0:
        dataDeterminazione = NOW

    root = lxml.html.fromstring(html )
    divs = root.cssselect("div[id='corpo']")
    for div in divs:
        print(div)
        for tr in div.cssselect("tr.riga"):
            #print(tr)        
            tds = tr.cssselect("td")
            #print(td.text)
            
            # estrae importo
            importoStr = ""
            importo = 0
            matchObj = re.match( r'.*EURO ([0-9\.,]*).*', tds[2].text_content(), re.M|re.I)
            if matchObj:
                print "matchObj.group(1) : ", matchObj.group(1)
                importoStr =  matchObj.group(1)
                if importoStr .endswith('.') or importoStr .endswith(',') :
                    importoStr = importoStr [:len(importoStr )-1]
                # trasfoma in numero
                if len(importoStr) > 2:
                    importoStr = importoStr .replace(".","")
                    importoStr = importoStr .replace(",",".")
                    importo = float(importoStr)
            else:
                print "No match!!"

            if len(tds)==3:
                data = {
                   'num' : tds[0].text_content(),
                   'codice' : tds[1].text_content(),
                   'importo' : importo ,
                   'anno' : int(tds[1].text_content()[:4]),
                   'descrizione' : tds[2].text_content(),
                   'DataSalvataggio' : dataDeterminazione.date(),
                   'DataUltimoUpdate' : NOW,
                   'url' : page
               }
                print data
                scraperwiki.sqlite.save(unique_keys=['codice'], data=data)

    return


baseUrl ="http://www.comune.torino.it/determinazioni/2012/"
htmlTot = scraperwiki.scrape(baseUrl)
rootTot = lxml.html.fromstring(htmlTot)
divsTot = rootTot.cssselect("div.riga")
for div in divsTot:
    links = div.cssselect('a')
    for link in links:
        url = link.get('href','')
        if url.startswith( '2012' ):
            print(url)
            scrapeSinglePage(baseUrl + url)




