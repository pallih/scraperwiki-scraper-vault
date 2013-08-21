# Am Anfang müssen wir ein paar Sachen importieren
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import scraperwiki


# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['venue', 'show', 'date', 'showDate', 'highestPrice', 'lowestPrice'])

# Webseite herunterladen
# (Das »"url%s" % char« ersetzt das »%s« im String durch die Variable char,
# wenn man das mit mehreren machen wollte, ginge das so: »"url%sblah%sblah%i" % (string, noch_ein_string, zahl)«)
website = scraperwiki.scrape("http://www.koka36.de/showevents.php")
# Neue Instanz von BeautifulSoup mit dem gerade heruntergeladenen Quelltext erstellen
soup = BeautifulSoup(website)

#print(website)

#print("----")
#print len(soup.find("a", "tipps" ))
#print("----")

for a in soup.findAll("a", "tipps" ):
    show = a.string
    print show 
    #print a['href']
    
    detailWebsite = scraperwiki.scrape("http://www.koka36.de" + a['href'])
    #print(detailWebsite)
    soup2 = BeautifulSoup(detailWebsite)
    for location in soup2.findAll("a", { "onfocus" : "if(this.blur)this.blur()" } ):
         if location.string is not None : 
            if location.string.find("Berlin") != -1 and len(location.string.split(":")) > 1: 
                venue = location.string.split(":")[1]
                print venue
    highPrice = 0.0
    lowPrice = 9999999999999
    for price in soup2.findAll("td", "hellgrau" ) :
        if price.string is not None : 
            if price.string.find("euro") != -1 : 
                priceValue = price.string[0:-18]
                print priceValue
                if priceValue.find("--") == -1 :
                    if highPrice <  float(priceValue) : 
                        highPrice = float(priceValue)
                    if lowPrice >  float(priceValue) : 
                        lowPrice = float(priceValue)
            if price.string.find("2011") != -1 : 
                dateValue = price.string
                print dateValue    
    print("HIGHEST PRICE:"+ str(highPrice))
    print("LOWEST PRICE:"+ str(lowPrice))
    
    if highPrice != 0 and venue is not None :
        record = {}
        record['venue'] = venue
        record['show'] = show
        if dateValue is not None : record['showDate'] = dateValue
        record['highestPrice'] = highPrice
        record['lowestPrice'] = lowPrice
        scraperwiki.datastore.save(["show","venue"], record)
    
    print("----")


