import urllib
import urlparse
import lxml.html
import re

#def part(alink):
#    html = urllib.urlopen(alink).read()
#    print html
#    root = lxml.html.fromstring(html)
#    h1 = root.cssselect("div#INHALT h1")[0].text
#    print h1
#    mh1 = re.match("Wahltermine in (.*?) seit (\d+)", h1)
#    assert mh1, h1
#    print mh1.group(1), mh1.group(2)
#    return
    
#    for tr in root.cssselect("div#INHALT tr"):
#        print lxml.html.tostring(tr)

#def Main():
    url = "http://www.bundeswahlleiter.de/de/landtagswahlen/wahltermine/"
#    url = "http://www.50hertz-transmission.net/de/165.htm"
    html = urllib.urlopen(url).read()
    print html
    
#    root = lxml.html.fromstring(html)
    
#    links = root.cssselect("div#INHALT li a")
#    for link in links:
#        alink = urlparse.urljoin(url, link.attrib.get("href"))
#        part(alink)

#Main()
#part("http://www.bundeswahlleiter.de/de/landtagswahlen/wahltermine/sachsen.html")
import urllib
import urlparse
import lxml.html
import re

#def part(alink):
#    html = urllib.urlopen(alink).read()
#    print html
#    root = lxml.html.fromstring(html)
#    h1 = root.cssselect("div#INHALT h1")[0].text
#    print h1
#    mh1 = re.match("Wahltermine in (.*?) seit (\d+)", h1)
#    assert mh1, h1
#    print mh1.group(1), mh1.group(2)
#    return
    
#    for tr in root.cssselect("div#INHALT tr"):
#        print lxml.html.tostring(tr)

#def Main():
    url = "http://www.bundeswahlleiter.de/de/landtagswahlen/wahltermine/"
#    url = "http://www.50hertz-transmission.net/de/165.htm"
    html = urllib.urlopen(url).read()
    print html
    
#    root = lxml.html.fromstring(html)
    
#    links = root.cssselect("div#INHALT li a")
#    for link in links:
#        alink = urlparse.urljoin(url, link.attrib.get("href"))
#        part(alink)

#Main()
#part("http://www.bundeswahlleiter.de/de/landtagswahlen/wahltermine/sachsen.html")
