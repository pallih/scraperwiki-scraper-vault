import scraperwiki
import datetime

# Blank Python

from bs4 import BeautifulSoup
from urllib2 import urlopen



BASE_URL = "http://receive-sms-online.com"


html = urlopen(BASE_URL).read()
soup = BeautifulSoup(html, "lxml")
#print soup
boccat = soup.find(id="content")
#print boccat 
#print soup.findAll("a")
now = datetime.datetime.now()
for hlink in boccat.findAll("a"):
    data = { 
             'title': "sms number",
             'description':  hlink.string,
             'link':  hlink.get('href'),
             'pubDate' : str(now),
        }
    scraperwiki.sqlite.save(unique_keys=['link'],data=data)




