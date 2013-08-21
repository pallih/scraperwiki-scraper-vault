import scraperwiki

from urlparse import urljoin
from BeautifulSoup import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

base = "http://www.victoria.ca/EN/main/city/mayor-council-committees/"
url = base + "councillors.html"
s = BeautifulSoup(scraperwiki.scrape(url))

def counc(u, mayor=False):

    record = {}
    record["source_url"] = u
    record["boundary_url"] = "/boundaries/census-subdivisions/5917034/"
    record["elected_office"] = u"Mayor" if mayor else u"Councillor"
    
    t = BeautifulSoup(scraperwiki.scrape(u))
    d = t.find("div", id="content")

    h1 = t.find("h1", id="headline")
    record["name"] = h1.text

    if mayor:
        record["name"] = " ".join(record["name"].split(" ")[1:])
        record["email"] = u"mayor@victoria.ca"
    else:
        ps = d.find("p")
        record["email"] = ps.find("a").text

    record["photo_url"] = urljoin(base, d.find("img")["src"])

    scraperwiki.sqlite.save(["name"], record)


c = s.find("div", id="content")
ehs = c.find("ul").findAll("a")

for a in ehs:
    counc(urljoin(base, a["href"]))

#mayor
counc("http://www.victoria.ca/EN/main/city/mayor-council-committees/mayor-dean-fortin.html", True)