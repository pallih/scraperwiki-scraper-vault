import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://thepagefinder.com/bentonville-ar/")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.page_item img"):           
      print lxml.html.tostring(el)
    