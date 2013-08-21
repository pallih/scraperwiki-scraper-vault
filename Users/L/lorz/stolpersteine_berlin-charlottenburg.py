import scraperwiki

# Blank Python
import lxml.html
html = scraperwiki.scrape("http://www.berlin.de/ba-charlottenburg-wilmersdorf/bezirk/lexikon/stolpersteine_strassen.html").decode('utf-8')
root = lxml.html.fromstring(html)


for el in root.cssselect("ul.bacontent a"):
    
    steinurl = 'http://berlin.de'+el.attrib['href']
    steinname = el.text

    print steinname
