import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)
print html
for el in root.cssselect("div.featured a"):
    print el
    print lxml.html.tostring(el)
    print el.attrib['href']
el = root.cssselect("div#footer_inner strong")
if el:
    print el[0]
    print el[0].text

