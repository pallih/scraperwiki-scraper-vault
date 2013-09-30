import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://www.hofvantwente.nl/bestuur-en-organisatie/gemeenteraad-en-commissies/samenstelling.html")
root = lxml.html.fromstring(html)
url = {}
i = 0
for link in root.cssselect("li.current-hassub a"):           
    url[i] = link.attrib['href']
    i += 1

j = 2
c = 0
d = 0
persoon = {}

colnames = {}
colnames[0] = 'Naam'
colnames[1] = 'Adres'
colnames[2] = 'Plaats'
colnames[3] = 'Telefoon'
colnames[4] = 'Mail'
colnames[5] = 'Bla'
colnames[6] = 'Bla2'

while(j < 9):
    html = scraperwiki.scrape("http://www.hofvantwente.nl/"+url[j])
    root = lxml.html.fromstring(html)
    for i in root.cssselect("div.one-col div h1,p"):
        if i.tag == 'h1':            
            if d == 1:
                scraperwiki.sqlite.save(unique_keys=[], data=persoon)
            c = 0
            persoon = {}
            d = 1
        if i.text != '':
            persoon[colnames[c]] = i.text
            c += 1
    j += 1

import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://www.hofvantwente.nl/bestuur-en-organisatie/gemeenteraad-en-commissies/samenstelling.html")
root = lxml.html.fromstring(html)
url = {}
i = 0
for link in root.cssselect("li.current-hassub a"):           
    url[i] = link.attrib['href']
    i += 1

j = 2
c = 0
d = 0
persoon = {}

colnames = {}
colnames[0] = 'Naam'
colnames[1] = 'Adres'
colnames[2] = 'Plaats'
colnames[3] = 'Telefoon'
colnames[4] = 'Mail'
colnames[5] = 'Bla'
colnames[6] = 'Bla2'

while(j < 9):
    html = scraperwiki.scrape("http://www.hofvantwente.nl/"+url[j])
    root = lxml.html.fromstring(html)
    for i in root.cssselect("div.one-col div h1,p"):
        if i.tag == 'h1':            
            if d == 1:
                scraperwiki.sqlite.save(unique_keys=[], data=persoon)
            c = 0
            persoon = {}
            d = 1
        if i.text != '':
            persoon[colnames[c]] = i.text
            c += 1
    j += 1

