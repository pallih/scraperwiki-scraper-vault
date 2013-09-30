import scraperwiki
import mechanize
import lxml.html           
from dateutil.parser import *
from datetime import *
from dateutil.relativedelta import *
import commands
import os
import re
from BeautifulSoup import BeautifulSoup



def scrapeSinglePage(page): 
    "scarica determinazioni da signole pagine"
    html = scraperwiki.scrape(page)
    #print html
    
    now = parse(commands.getoutput("date"))
    today = now.date()
    NOW = datetime.now()

    #dataDeterminazione = getDateDeterminazione(page)
    #print(dataDeterminazione)
    #if relativedelta(dataDeterminazione, NOW) > 0:
    #    dataDeterminazione = NOW

    root = lxml.html.fromstring(html )
    divs = root.cssselect("div[id='ctl00_mainIndexContent_pnlRisultati']")
    rowcount = 0
    for div in divs:
        print(div)
        for tr in div.cssselect("tr.item"+str(rowcount)):
            if rowcount==0:
                rowcount = 1
            else :
                rowcount = 0                    
            tds = tr.cssselect("td")
            links = tds[0].cssselect("a")
            description = links[0].text
            print(description)
            print(tds[1].text)
            print(tds[2].text_content()[-4:])
            print(tds[2].text_content()[-10:])
            print(tds[2].text)
            print(tds[3].text)
            
            # estrae importo
            importoStr = ""
            importo = 0
            matchObj = re.match( r'.*EURO([\s0-9\.,]*).*', description, re.M|re.I)
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

            # formatta data
            dataStr =  tds[2].text_content()[-10:]
            anno = dataStr[6:]
            dataStr =  tds[2].text_content()[-10:]
            mese = dataStr[3:]
            mese = mese[:2]
            dataStr =  tds[2].text_content()[-10:]
            giorno = dataStr[:2]
            print(tds[2].text_content())
            print(anno)
            print(mese)
            print(giorno)
            dataDelibera = datetime.strptime(anno + "-" + mese + "-" + giorno, '%Y-%m-%d') 

            #ripulisci descrizione delibere
            description = description.strip()
            description = description.replace("\n","")
            if len(tds)==4:
                data = {
                   'num' : "",
                   'codice' : tds[2].text_content().strip(),
                   'importo' : importo ,
                   'categoria' : tds[1].text_content().strip(),
                   'anno' : int(tds[2].text_content()[-4:]),
                   'descrizione' : description,
                   'DataSalvataggio' : dataDelibera.date() ,
                   'DataUltimoUpdate' : NOW,
                   'url' : page
               }
                print data
                scraperwiki.sqlite.save(unique_keys=['codice'], data=data)
        
    return


baseUrl ="http://www.comune.milano.it/albopretorio/AlboPretorioWeb/AlboPretorio.aspx"
scrapeSinglePage(baseUrl)
import scraperwiki
import mechanize
import lxml.html           
from dateutil.parser import *
from datetime import *
from dateutil.relativedelta import *
import commands
import os
import re
from BeautifulSoup import BeautifulSoup



def scrapeSinglePage(page): 
    "scarica determinazioni da signole pagine"
    html = scraperwiki.scrape(page)
    #print html
    
    now = parse(commands.getoutput("date"))
    today = now.date()
    NOW = datetime.now()

    #dataDeterminazione = getDateDeterminazione(page)
    #print(dataDeterminazione)
    #if relativedelta(dataDeterminazione, NOW) > 0:
    #    dataDeterminazione = NOW

    root = lxml.html.fromstring(html )
    divs = root.cssselect("div[id='ctl00_mainIndexContent_pnlRisultati']")
    rowcount = 0
    for div in divs:
        print(div)
        for tr in div.cssselect("tr.item"+str(rowcount)):
            if rowcount==0:
                rowcount = 1
            else :
                rowcount = 0                    
            tds = tr.cssselect("td")
            links = tds[0].cssselect("a")
            description = links[0].text
            print(description)
            print(tds[1].text)
            print(tds[2].text_content()[-4:])
            print(tds[2].text_content()[-10:])
            print(tds[2].text)
            print(tds[3].text)
            
            # estrae importo
            importoStr = ""
            importo = 0
            matchObj = re.match( r'.*EURO([\s0-9\.,]*).*', description, re.M|re.I)
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

            # formatta data
            dataStr =  tds[2].text_content()[-10:]
            anno = dataStr[6:]
            dataStr =  tds[2].text_content()[-10:]
            mese = dataStr[3:]
            mese = mese[:2]
            dataStr =  tds[2].text_content()[-10:]
            giorno = dataStr[:2]
            print(tds[2].text_content())
            print(anno)
            print(mese)
            print(giorno)
            dataDelibera = datetime.strptime(anno + "-" + mese + "-" + giorno, '%Y-%m-%d') 

            #ripulisci descrizione delibere
            description = description.strip()
            description = description.replace("\n","")
            if len(tds)==4:
                data = {
                   'num' : "",
                   'codice' : tds[2].text_content().strip(),
                   'importo' : importo ,
                   'categoria' : tds[1].text_content().strip(),
                   'anno' : int(tds[2].text_content()[-4:]),
                   'descrizione' : description,
                   'DataSalvataggio' : dataDelibera.date() ,
                   'DataUltimoUpdate' : NOW,
                   'url' : page
               }
                print data
                scraperwiki.sqlite.save(unique_keys=['codice'], data=data)
        
    return


baseUrl ="http://www.comune.milano.it/albopretorio/AlboPretorioWeb/AlboPretorio.aspx"
scrapeSinglePage(baseUrl)
