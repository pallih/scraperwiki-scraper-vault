import scraperwiki
import lxml.html
#source = "http://www.energiamarkkinavirasto.fi/data.asp?articleid=3116&pgid=40&languageid=246"
source = "http://www.energiamarkkinavirasto.fi/data.asp?articleid=3328&pgid=40&languageid=246"
html = scraperwiki.scrape(source)
root = lxml.html.fromstring(html)

nodes = [el for el in root.cssselect('tr[style]')]
organizations = []
for n in nodes[2:]:
    org = []
    for t in  n.cssselect('td[style] p[class][style] span[style]'):
        if t.text:
            org.append(t.text)
    print org[0].encode("iso8859-1"), org[1], org[2], org[3], org[4]
    organizations.append(org)

keys = ("yritys", "katuosoite", "postinumero", "kaupunki", "puhelinnumero")

for org in organizations:
    orgdata = dict(zip(keys,org))
    scraperwiki.sqlite.save(unique_keys=["yritys"], data=orgdata)
import scraperwiki
import lxml.html
#source = "http://www.energiamarkkinavirasto.fi/data.asp?articleid=3116&pgid=40&languageid=246"
source = "http://www.energiamarkkinavirasto.fi/data.asp?articleid=3328&pgid=40&languageid=246"
html = scraperwiki.scrape(source)
root = lxml.html.fromstring(html)

nodes = [el for el in root.cssselect('tr[style]')]
organizations = []
for n in nodes[2:]:
    org = []
    for t in  n.cssselect('td[style] p[class][style] span[style]'):
        if t.text:
            org.append(t.text)
    print org[0].encode("iso8859-1"), org[1], org[2], org[3], org[4]
    organizations.append(org)

keys = ("yritys", "katuosoite", "postinumero", "kaupunki", "puhelinnumero")

for org in organizations:
    orgdata = dict(zip(keys,org))
    scraperwiki.sqlite.save(unique_keys=["yritys"], data=orgdata)
