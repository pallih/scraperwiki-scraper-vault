import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)


for el in root.cssselect("div.featured a"):
    print el


    print lxml.html.tostring(el)

    print el.attrib['href']