import scraperwiki           
html = scraperwiki.scrape("https://sites.google.com/site/eataroundhk/1")

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[dir='ltr'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==2:
        number = tds[0].text
        address = tds[1].text
        
        data = {
            'number' : number,
            'address' : address
        }

        scraperwiki.sqlite.save(unique_keys=['number'], data=data)import scraperwiki           
html = scraperwiki.scrape("https://sites.google.com/site/eataroundhk/1")

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[dir='ltr'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==2:
        number = tds[0].text
        address = tds[1].text
        
        data = {
            'number' : number,
            'address' : address
        }

        scraperwiki.sqlite.save(unique_keys=['number'], data=data)