import scraperwiki
import lxml.html
import lxml.etree

html = scraperwiki.scrape("https://legalmarijuanadispensary.com/dispensaries/in/washington")
root = lxml.html.fromstring(html)

y = 0
while y < 12:
    y += 1 
    for elt in root.cssselect("div [class='listings']"):
        url = "https://legalmarijuanadispensary.com" + elt.getchildren()[y].getchildren()[0].getchildren()[0].attrib['href']
        data = {
            'url': url,
        }
        scraperwiki.sqlite.save(unique_keys=['url'],data=data)
