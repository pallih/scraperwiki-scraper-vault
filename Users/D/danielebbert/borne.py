import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://gemeenteraad.borne.nl/Gemeenteraad")
root = lxml.html.fromstring(html)
url = {}
i = 0
for link in root.cssselect("a.name"):           
    url[i] = link.attrib['href']
    i += 1

j = 0
c = 0

persoon = {}
colnames = {}
colnames[0] = '0'
colnames[1] = '1'
colnames[2] = '2'
colnames[3] = '3'
colnames[4] = '4'
colnames[5] = '5'
colnames[6] = '6'


while(j < 19):
    html = scraperwiki.scrape("http://gemeenteraad.borne.nl/"+url[j])
    root = lxml.html.fromstring(html)
    for i in root.cssselect("div.medewerkerpagina h2,span.waarde,div.description p"):                   
        print i.text,c
        if c < 7:
            persoon[colnames[c]] = i.text
        else:
            scraperwiki.sqlite.save(unique_keys=[], data=persoon)
            persoon = {}
            c = 0
            persoon[colnames[c]] = i.text
        c += 1
    j += 1
