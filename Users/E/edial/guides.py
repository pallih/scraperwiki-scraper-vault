import scraperwiki
import lxml.html           

html = scraperwiki.scrape("http://f.cl.ly/items/0j0p242L2A2R283W2W46/source_code.html")
print html

root = lxml.html.fromstring(html)


for el in root.cssselect("div. a"):           
    print el

    print lxml.html.tostring(el)

    print el.attrib['href']
