import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
import time
import scraperwiki
import requests
import BeautifulSoup
import time
import re

def scrape_site():
    url = "https://www.citeecar.com/views/Locations.jsf"

    html = requests.get(url, verify = False).text
    root = lxml.html.fromstring(html)
    print root.cssselect("div #locationResultListHandler")[0]
    #el = root.xpath("//p[@class='data-spotAddress small_grey4']")
    #print el[0].text
    #for i in range(len(root[0])):
        #print root[0][i].cssselect("h2")
#"data-spotAddress small_grey4"
            #print root.("div #locationItem_5695")[0].text
    
   
def main():
   
    scrape_site()
     

main()

import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
import time
import scraperwiki
import requests
import BeautifulSoup
import time
import re

def scrape_site():
    url = "https://www.citeecar.com/views/Locations.jsf"

    html = requests.get(url, verify = False).text
    root = lxml.html.fromstring(html)
    print root.cssselect("div #locationResultListHandler")[0]
    #el = root.xpath("//p[@class='data-spotAddress small_grey4']")
    #print el[0].text
    #for i in range(len(root[0])):
        #print root[0][i].cssselect("h2")
#"data-spotAddress small_grey4"
            #print root.("div #locationItem_5695")[0].text
    
   
def main():
   
    scrape_site()
     

main()

