import scraperwiki
import lxml.html

# Blank Python

html = scraperwiki.scrape('http://www.ipchicken.com/')
page = lxml.html.fromstring(html)
print(html)
