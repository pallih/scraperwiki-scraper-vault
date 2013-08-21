import scraperwiki

# Blank Python
import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector

def scrape_site():
    url = "http://de.drive-now.com/static/metropolis/js/Map.js"
    html = requests.get(url, verify = False).text
    
    root = lxml.html.fromstring(html)
    print root.cssselect("li")[0].text_content()



def main():
    for id in range(1):
        scrape_site()

main()
