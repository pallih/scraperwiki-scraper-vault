import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.nuforc.org/webreports/ndxe201205.html")
root = lxml.html.fromstring(html)
for el in root:
    print el.tag
    for el2 in el:
        print "--", el2.tag, el2.attrib




