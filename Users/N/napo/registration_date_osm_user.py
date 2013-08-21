import scraperwiki
import lxml.html 
url = "http://www.openstreetmap.org/user/simone"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html) 
registration_date = root.cssselect("p.deemphasize")[1].text_content().split("|")[0].split(": ")[1]
print registration_date
