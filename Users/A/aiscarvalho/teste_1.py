import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://lazer.publico.pt")
root = lxml.html.fromstring(html)

for el in root.cssselect(".featnews-thumbright a"):
     print el.attrib['title']

