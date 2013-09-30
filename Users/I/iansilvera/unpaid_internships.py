import scraperwiki           
import lxml.html
html = scraperwiki.scrape("https://www.work4mp.com/")
root = lxml.html.fromstring(html)
for el in root.cssselect("div.intern a"):           
    print el
 print lxml.html.tostring(el)
  print el.attrib['href']import scraperwiki           
import lxml.html
html = scraperwiki.scrape("https://www.work4mp.com/")
root = lxml.html.fromstring(html)
for el in root.cssselect("div.intern a"):           
    print el
 print lxml.html.tostring(el)
  print el.attrib['href']