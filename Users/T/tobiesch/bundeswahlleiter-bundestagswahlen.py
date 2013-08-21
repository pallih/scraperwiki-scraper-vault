import urllib
import urlparse
import lxml.html
import re
import scraperwiki
import datetime

months = [u"Januar", u"Februar", u"M\xe4rz", u"April", u"Mai", u"Juni", u"Juli", u"August", u"September", u"Oktober", u"November", u"Dezember"]
def convertdate(d):
    #print "date is ", [d]
    d=re.sub('\xa0',' ',d)
    print "date is ", [d]
    md = re.match("(?u)(\d+)\. (\w+) (\d+)$", d)
    #print "month is ", [md.group(2)]
    imonth = months.index(md.group(2)) + 1
    return datetime.date(int(md.group(3)), imonth, int(md.group(1)))

def part(alink):
    html = urllib.urlopen(alink).read()
    print html
    root = lxml.html.fromstring(html)
    h1 = root.cssselect("div#INHALT h1.Section1")[0].text
    mh1 = re.match("Wahl zum (\d+)\. (.*?) am (.*)", h1)
    assert mh1, h1
    print mh1.group(1), mh1.group(2), mh1.group(3)
    
    data = { "electionnr":mh1.group(1), "parliament":"Deutscher Bundestag", "date":convertdate(mh1.group(3)), "source":alink}

    print data
    scraperwiki.sqlite.save(["parliament", "date"], data)




def Main():
    url = "http://www.bundeswahlleiter.de/de/bundestagswahlen/fruehere_bundestagswahlen/"
    
    html = urllib.urlopen(url).read()
    print html
    
    root = lxml.html.fromstring(html)
    
    links = root.cssselect("div#NAVIGATION div.level1 li a")

    for link in links:
        alink = urlparse.urljoin(url, link.attrib.get("href"))
        #print alink
        part(alink)
    


Main()
#part("http://www.bundeswahlleiter.de/de/landtagswahlen/wahltermine/sachsen.html")