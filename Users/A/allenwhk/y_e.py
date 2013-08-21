import scraperwiki           
#html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
html = scraperwiki.scrape("http://biz.yahoo.com/research/earncal/20120823.html")
print html
import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table"):
    tds = tr.cssselect("td")
    print tds[0].text_content()