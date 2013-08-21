import scraperwiki
import scraperwiki           
import lxml.html
import uuid
import datetime
    
html = scraperwiki.scrape('http://www.wipo.int/amc/en/domains/search/text.jsp?case=D2013-0001')
root = lxml.html.fromstring(html)
for title in root.cssselect("span[id='c-col']"):  



