import scraperwiki
import urlparse
import lxml.html
import re
from BeautifulSoup import BeautifulSoup
from lxml.html import fromstring

url = "http://www.ymcans.org.uk/whats-going-on/whats-on/"

webPage = 'http://www.ymcans.org.uk'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
#print root
soup = BeautifulSoup(html)
#print soup    
events = soup.findAll('div', { "class" : "event njscal active" })  
print events

        
table_cell = soup.findAll('h4')
print table_cell

         
    

