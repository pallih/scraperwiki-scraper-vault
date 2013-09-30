# Am Anfang müssen wir ein paar Sachen importieren
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import scraperwiki


# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['id', 'title'])

# Webseite herunterladen
# (Das »"url%s" % char« ersetzt das »%s« im String durch die Variable char,
# wenn man das mit mehreren machen wollte, ginge das so: »"url%sblah%sblah%i" % (string, noch_ein_string, zahl)«)
website = scraperwiki.scrape("http://tickets.shop.ebay.de/Festivals-Konzerte-/34814/i.html?Stadt=Berlin&_trkparms=65%253A12%257C66%253A4%257C39%253A1%257C72%253A4344&rt=nc&_catref=1&_dmpt=Festivals_Konzerte_1&_ipg=999999&_trksid=p3286.c0.m14.l1581&_pgn=1")
# Neue Instanz von BeautifulSoup mit dem gerade heruntergeladenen Quelltext erstellen
soup = BeautifulSoup(website)

#print(website)

#print("----")
#print len(soup.find("a", "tipps" ))
#print("----")

#<li class="toppg-t">Seite 3 von 3</li>
for li in soup.findAll("li", "toppg-t") : 
    pages = li.string.split(" von ")[1]
    print ("PAGES: " + pages)
    for page in range(1, int(pages)+1):
        print ("PAGE: " + str(page))
        website = scraperwiki.scrape("http://tickets.shop.ebay.de/Festivals-Konzerte-/34814/i.html?Stadt=Berlin&_trkparms=65%253A12%257C66%253A4%257C39%253A1%257C72%253A4344&rt=nc&_catref=1&_dmpt=Festivals_Konzerte_1&_ipg=999999&_trksid=p3286.c0.m14.l1581&_pgn="+pages)
        soup2 = BeautifulSoup(website)
        
        for a in soup2.findAll("a", "vip" ):
            title = a.string
            href = a["href"]
            id = href.split("/")[4].split("?")[0]
            print title
            print id
        
            record = {}
            record['id'] = id
            record['title'] = title
            
        
            scraperwiki.datastore.save(["id"], record)
            print("----")
        print("-----------------------------------------")
        

# Am Anfang müssen wir ein paar Sachen importieren
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import scraperwiki


# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['id', 'title'])

# Webseite herunterladen
# (Das »"url%s" % char« ersetzt das »%s« im String durch die Variable char,
# wenn man das mit mehreren machen wollte, ginge das so: »"url%sblah%sblah%i" % (string, noch_ein_string, zahl)«)
website = scraperwiki.scrape("http://tickets.shop.ebay.de/Festivals-Konzerte-/34814/i.html?Stadt=Berlin&_trkparms=65%253A12%257C66%253A4%257C39%253A1%257C72%253A4344&rt=nc&_catref=1&_dmpt=Festivals_Konzerte_1&_ipg=999999&_trksid=p3286.c0.m14.l1581&_pgn=1")
# Neue Instanz von BeautifulSoup mit dem gerade heruntergeladenen Quelltext erstellen
soup = BeautifulSoup(website)

#print(website)

#print("----")
#print len(soup.find("a", "tipps" ))
#print("----")

#<li class="toppg-t">Seite 3 von 3</li>
for li in soup.findAll("li", "toppg-t") : 
    pages = li.string.split(" von ")[1]
    print ("PAGES: " + pages)
    for page in range(1, int(pages)+1):
        print ("PAGE: " + str(page))
        website = scraperwiki.scrape("http://tickets.shop.ebay.de/Festivals-Konzerte-/34814/i.html?Stadt=Berlin&_trkparms=65%253A12%257C66%253A4%257C39%253A1%257C72%253A4344&rt=nc&_catref=1&_dmpt=Festivals_Konzerte_1&_ipg=999999&_trksid=p3286.c0.m14.l1581&_pgn="+pages)
        soup2 = BeautifulSoup(website)
        
        for a in soup2.findAll("a", "vip" ):
            title = a.string
            href = a["href"]
            id = href.split("/")[4].split("?")[0]
            print title
            print id
        
            record = {}
            record['id'] = id
            record['title'] = title
            
        
            scraperwiki.datastore.save(["id"], record)
            print("----")
        print("-----------------------------------------")
        

