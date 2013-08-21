# Blank Python
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import scraperwiki

for i in range(11900,13600,100):
    url = "http://www.spoj.pl/ranks/users/start=%d" % i
    request = urllib2.urlopen(url)
    html = request.read()
    soup = BeautifulSoup(html)
    links = soup.findAll('a',{'href' : re.compile("/*/users/+")})
    for j in links:
        s = str(j)
        k = s.find("users/")
        l = s.find("\">")
        s = s[k:l]
        request = urllib2.urlopen("http://www.spoj.pl/" + s + "/")
        html = request.read()
        soup = BeautifulSoup(html)
        s = soup.find(text = 'E-mail:')
        if (s != None):
            s =  str(s.findNext('a'))
            k = s.rfind("\">")
            l = s.rfind("<")
            s = s[(k+2):l]
            s = s.replace("[at]","@")
            s = s.replace("[dot]",".")
            scraperwiki.datastore.save(unique_keys=['Email'], data={'Email':s})
