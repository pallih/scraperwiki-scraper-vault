# scrap les titres cliquables de la page correspondant à la balise <a ...>

import scraperwiki
import time
import urllib2,sys
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString

#define page range to be scrapped 
NbPage = range(0, 1)

#provide the common part of the urls to be scrapped
AddressInit = "https://market.android.com/details?id=apps_topselling_free&start="

#a function to log the interresting information, here the title of the app with an appropriate id...
def printText(tags):
    for tag in tags:
        if (tag.__class__ == NavigableString):
            if (tag != "&nbsp;") and (tag != "Installer"):
                t=time.time()
                data = {
                    'tag' : tag,
                    'timestamp' : t
                    }
                scraperwiki.sqlite.save(unique_keys=["timestamp"], data= data, table_name="yan")  
            
        else:
            printText(tag)
    



for i in NbPage:

    Address=str(AddressInit)+str(i)+'&num=24&hl=fr'

    html = urllib2.urlopen(Address).read()

    soup = BeautifulSoup(html)

    cle=1+i*10000

    printText(soup.findAll('div',"goog-inline-block"))
    # scrap les titres cliquables de la page correspondant à la balise <a ...>

import scraperwiki
import time
import urllib2,sys
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString

#define page range to be scrapped 
NbPage = range(0, 1)

#provide the common part of the urls to be scrapped
AddressInit = "https://market.android.com/details?id=apps_topselling_free&start="

#a function to log the interresting information, here the title of the app with an appropriate id...
def printText(tags):
    for tag in tags:
        if (tag.__class__ == NavigableString):
            if (tag != "&nbsp;") and (tag != "Installer"):
                t=time.time()
                data = {
                    'tag' : tag,
                    'timestamp' : t
                    }
                scraperwiki.sqlite.save(unique_keys=["timestamp"], data= data, table_name="yan")  
            
        else:
            printText(tag)
    



for i in NbPage:

    Address=str(AddressInit)+str(i)+'&num=24&hl=fr'

    html = urllib2.urlopen(Address).read()

    soup = BeautifulSoup(html)

    cle=1+i*10000

    printText(soup.findAll('div',"goog-inline-block"))
    