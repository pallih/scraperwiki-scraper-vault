# Import Thing
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import scraperwiki
import cookielib

username = 'webscrape'
password = 'testing'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'Email_Address' : username, 'Password' : password})
opener.open('http://www.ha.com/common/login.php?bypassSSL=1', login_data)
resp = opener.open('http://www.ha.com')
print resp



#http://www.ha.com/common/login.php?headerlink=true


# define the order our columns are displayed in the datastore
scraperwiki.sqlite.save_var('data_columns', ['id', 'title'])

# Website Download
# (The »"url%s" % char« replace this »%s« in the String by the Variable char,
# if you wanted to do with with several, it would look like: »"url%sblah%sblah%i" % (string, more_string, number)«)
website = scraperwiki.scrape("http://historical.ha.com/common/search_results.php?Ne=2012&N=49+790+231+2227&erpp=50")
# Neue Instanz von BeautifulSoup mit dem gerade heruntergeladenen Quelltext erstellen
soup = BeautifulSoup(website)

print(website)

#print("----")
#print len(soup.find("a", "tipps" ))
#print("----")

#<li class="toppg-t">Seite 3 von 3</li>
for div in soup.findAll("div", "lot-info ") : 
#        print div
#    pages = li.string.split(" von ")[1]
#    print ("PAGES: " + pages)
#    for page in range(1, int(pages)+1):
#        print ("PAGE: " + str(page))
#        website = scraperwiki.scrape("http://www.ebay.de/sch/Festivals-Konzerte-/34814/i.html?Stadt=Berlin&_trkparms=65%253A12%257C66%253A4%257C39%253A1%257C72%253A4344&rt=nc&_catref=1&_dmpt=Festivals_Konzerte_1&_ipg=999999&_trksid=p3286.c0.m14.l1581&_pgn="+pages)
        soup2 = BeautifulSoup(website)
        
        for varib in soup2.findAll("div", "description" ):
            title = varib.string
            href = varib.string
            id = href
            print title
            print id
        
            record = {}
            record['id'] = id
            record['title'] = title
            
        
            scraperwiki.sqlite.save(id, record)
            print("----")
        print("-----------------------------------------")
        

# Import Thing
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import scraperwiki
import cookielib

username = 'webscrape'
password = 'testing'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'Email_Address' : username, 'Password' : password})
opener.open('http://www.ha.com/common/login.php?bypassSSL=1', login_data)
resp = opener.open('http://www.ha.com')
print resp



#http://www.ha.com/common/login.php?headerlink=true


# define the order our columns are displayed in the datastore
scraperwiki.sqlite.save_var('data_columns', ['id', 'title'])

# Website Download
# (The »"url%s" % char« replace this »%s« in the String by the Variable char,
# if you wanted to do with with several, it would look like: »"url%sblah%sblah%i" % (string, more_string, number)«)
website = scraperwiki.scrape("http://historical.ha.com/common/search_results.php?Ne=2012&N=49+790+231+2227&erpp=50")
# Neue Instanz von BeautifulSoup mit dem gerade heruntergeladenen Quelltext erstellen
soup = BeautifulSoup(website)

print(website)

#print("----")
#print len(soup.find("a", "tipps" ))
#print("----")

#<li class="toppg-t">Seite 3 von 3</li>
for div in soup.findAll("div", "lot-info ") : 
#        print div
#    pages = li.string.split(" von ")[1]
#    print ("PAGES: " + pages)
#    for page in range(1, int(pages)+1):
#        print ("PAGE: " + str(page))
#        website = scraperwiki.scrape("http://www.ebay.de/sch/Festivals-Konzerte-/34814/i.html?Stadt=Berlin&_trkparms=65%253A12%257C66%253A4%257C39%253A1%257C72%253A4344&rt=nc&_catref=1&_dmpt=Festivals_Konzerte_1&_ipg=999999&_trksid=p3286.c0.m14.l1581&_pgn="+pages)
        soup2 = BeautifulSoup(website)
        
        for varib in soup2.findAll("div", "description" ):
            title = varib.string
            href = varib.string
            id = href
            print title
            print id
        
            record = {}
            record['id'] = id
            record['title'] = title
            
        
            scraperwiki.sqlite.save(id, record)
            print("----")
        print("-----------------------------------------")
        

