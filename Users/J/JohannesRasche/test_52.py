# JohannesRasche /  
import urllib
import urlparse
import lxml.html
import re
import scraperwiki

def part(alink):
    html = urllib.urlopen(alink).read()
    print html
    root = lxml.html.fromstring(html)
    h1 = root.cssselect("div#INHALT h1")[0].text
    print h1
    mh1 = re.match("Wahltermine i[nm] (.*?) seit (\d+)", h1)
    assert mh1, h1
    print mh1.group(1), mh1.group(2)
    
    currentlhc = None
    nextnumber = 0
    for tr in root.cssselect("div#INHALT tr"):
        td0 = tr[0]
        td1 = tr[1]
        if re.match("\s*$", td1.text) or td1.text == u'\xa0':
            nextnumber += 1
            continue
        if td1.text[-4:] == 'Wahl':
            currentlhc = re.sub(".*\.\.\.\s*", "", td0.text)
            nextnumber = 1
            continue
        assert td0.text == "%d." % nextnumber, (td0.text, nextnumber)
        nextnumber += 1
        data = { "state":mh1.group(1), "parliament":currentlhc, "date":td1.text, "source":alink}
        print data
        scraperwiki.sqlite.save(["state", "parliament", "date"], data)

def Main():
    url = "http://www.bundeswahlleiter.de/de/künftige_wahlen/"
    
    html = urllib.urlopen(url).read()
    print html
    
    root = lxml.html.fromstring(html)
    
    links = root.cssselect("div#INHALT li a")
    for link in links:
        alink = urlparse.urljoin(url, link.attrib.get("href"))
        part(alink)

Main()
#part("http://www.bundeswahlleiter.de/de/künftige_wahlen/")
