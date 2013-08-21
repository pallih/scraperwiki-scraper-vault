# Blank Python
import scraperwiki
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re

for i in range(8850,28200,25):
    url = "http://acm.tju.edu.cn/toj/ranklist.php?start=%d" % i
    request = urllib2.urlopen(url)
    html = request.read()
    soup = BeautifulSoup(html)
    links = soup.findAll('a',{'href' : re.compile("/*user_+")})
    for j in links:
        s = str(j)
        k = s.find("user_")
        l = s.find("\">")
        s = s[k:l]
        request = urllib2.urlopen("http://acm.tju.edu.cn/toj/" + s)
        html = request.read()
        soup = BeautifulSoup(html)
        s = soup.find(text = 'E-mail:&nbsp;').findNext('a')
        s = str(s)
        k = s.rfind("\">")
        l = s.rfind("<")
        s = s[(k+2):l]
        if (re.search(">*(Runs Status)+<",s) == None):
            scraperwiki.datastore.save(unique_keys=['Email'], data={'Email':s})
