import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import scraperwiki

url = "http://acm.sgu.ru/teaminfo.php"

data = {}
scraped_results = []

for i in range(20812,20814):
    data ['id'] = str ('%(ids)06d' % {"ids" : i})
    print data
    data_encoded = urllib.urlencode(data)
    request = urllib2.urlopen(url,data_encoded)
    html = request.read()
    soup = BeautifulSoup(html)
    s = soup.find(text = 'E-Mail')
    if (s != None):
        s =  str(s.findNext('td'))
        if (re.search(">*(Not available)+<",s) == None):
            j = s.find(';')
            k = s.rfind('<')
            s = s[(j+1):k]
            s = s.replace("[at]","@")
            s = s.replace("[dot]",".")
            scraperwiki.datastore.save(unique_keys=['Email'], data={'Email':s})
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import scraperwiki

url = "http://acm.sgu.ru/teaminfo.php"

data = {}
scraped_results = []

for i in range(20812,20814):
    data ['id'] = str ('%(ids)06d' % {"ids" : i})
    print data
    data_encoded = urllib.urlencode(data)
    request = urllib2.urlopen(url,data_encoded)
    html = request.read()
    soup = BeautifulSoup(html)
    s = soup.find(text = 'E-Mail')
    if (s != None):
        s =  str(s.findNext('td'))
        if (re.search(">*(Not available)+<",s) == None):
            j = s.find(';')
            k = s.rfind('<')
            s = s[(j+1):k]
            s = s.replace("[at]","@")
            s = s.replace("[dot]",".")
            scraperwiki.datastore.save(unique_keys=['Email'], data={'Email':s})
