import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup , SoupStrainer
import re

def extract_categories(soup):
    table = soup.find("table", width=334)
    for row in table.findAll('tr'):        
        #col = row.findAll('td')           
        links = row.findAll('a')
        print links.text
        print linls.url

mech = Browser()

url = "http://www.hotairac.com/Products.html"

page1 = mech.open(url)
html1 = page1.read()
soup = BeautifulSoup(html1)

extract_categories(soup)
