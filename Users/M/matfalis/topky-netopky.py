import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.skyscanner.net/flights/bts/prg/130407/130420/airfares-from-bratislava-to-prague-in-april-2013.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("span[class='px GBP']"):
    print tr
