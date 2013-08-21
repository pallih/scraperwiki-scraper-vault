import scraperwiki

# Blank Python
import scraperwiki           
import lxml.html
import urllib

webquery = "http://www.marinetraffic.com/ais/datasheet.aspx?MMSI=311012700&TIMESTAMP=2&datasource=POS"
html = scraperwiki.scrape(webquery)
root = lxml.html.fromstring(html)

for el in root.cssselect("div#datasheet a"): print el 
print html 