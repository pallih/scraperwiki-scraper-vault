import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
from BeautifulSoup import BeautifulSoup
# Blank Python


def scrape_site(id):
    url = "http://fussball.de-vereine.de/linkliste/fussball/fussballvereine/details/" + str(id)
    html = requests.get(url, verify = False).text
    
    root = lxml.html.fromstring(html)

    if root.cssselect("table")[2][2].text_content().split()[0] != "PLZ,":
        #name = None
        #maste hitta rätt tr om de tillhör rätt avdelning i listan, bundesland, spielt in kreis
        try:
            name_list =  root.cssselect("table")[2][0].text_content().split()[3:]
            name = ' '.join(name_list)
            print name 
        except: IndexError
        
        try:
            street = root.cssselect("table")[2][2].text_content().split(":")[1]

        except: IndexError

        try: 
            plz = root.cssselect("table")[2][3].text_content().split(":")[1].split()[0]
            city = root.cssselect("table")[2][3].text_content().split(":")[1].split()[1]
        
        except: IndexError

        data = {'id' : id,
                'street' : street,
                'plz' : plz,
                'city' : city, 
                'name' : name} 

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def main():
    for id in range(500,520):
        scrape_site(id)

main()
    
import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
from BeautifulSoup import BeautifulSoup
# Blank Python


def scrape_site(id):
    url = "http://fussball.de-vereine.de/linkliste/fussball/fussballvereine/details/" + str(id)
    html = requests.get(url, verify = False).text
    
    root = lxml.html.fromstring(html)

    if root.cssselect("table")[2][2].text_content().split()[0] != "PLZ,":
        #name = None
        #maste hitta rätt tr om de tillhör rätt avdelning i listan, bundesland, spielt in kreis
        try:
            name_list =  root.cssselect("table")[2][0].text_content().split()[3:]
            name = ' '.join(name_list)
            print name 
        except: IndexError
        
        try:
            street = root.cssselect("table")[2][2].text_content().split(":")[1]

        except: IndexError

        try: 
            plz = root.cssselect("table")[2][3].text_content().split(":")[1].split()[0]
            city = root.cssselect("table")[2][3].text_content().split(":")[1].split()[1]
        
        except: IndexError

        data = {'id' : id,
                'street' : street,
                'plz' : plz,
                'city' : city, 
                'name' : name} 

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def main():
    for id in range(500,520):
        scrape_site(id)

main()
    
