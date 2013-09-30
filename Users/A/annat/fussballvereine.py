import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
import time


def scrape_site(id):
    url = "http://fussball.de-vereine.de/linkliste/fussball/fussballvereine/details/" + str(id)
    html = requests.get(url, verify = False).text
    
    root = lxml.html.fromstring(html)
 
    
    if root.cssselect("table")[2][2].text_content().split()[0] != "PLZ,":
       
        try:
            name_list =  root.cssselect("table")[2][0].text_content().split()[3:]
            name = ' '.join(name_list)
           
        except IndexError:
            name = None
        
        try:
            street = root.cssselect("table")[2][2].text_content().split(":")[1]

        except IndexError: 
            street = None

        try: 
            plz = root.cssselect("table")[2][3].text_content().split(":")[1].split()[0]
            city = root.cssselect("table")[2][3].text_content().split(":")[1].split()[1]
        
        except IndexError: 
            plz = None
            city = None
        
        try:
            webpage = "http://fussball.de-vereine.de/link.php?id="+str(id)
            
        except IndexError: webpage = None
        
       # print url
        
        data = {'id' : id,
                'street' : street,
                'plz' : plz,
                'city' : city, 
                'name' : name,
                'webpage' : webpage
                } 

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def main():
    for id in range(6500):
        scrape_site(id)
        #time.sleep(5)

main()
    


import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
import time


def scrape_site(id):
    url = "http://fussball.de-vereine.de/linkliste/fussball/fussballvereine/details/" + str(id)
    html = requests.get(url, verify = False).text
    
    root = lxml.html.fromstring(html)
 
    
    if root.cssselect("table")[2][2].text_content().split()[0] != "PLZ,":
       
        try:
            name_list =  root.cssselect("table")[2][0].text_content().split()[3:]
            name = ' '.join(name_list)
           
        except IndexError:
            name = None
        
        try:
            street = root.cssselect("table")[2][2].text_content().split(":")[1]

        except IndexError: 
            street = None

        try: 
            plz = root.cssselect("table")[2][3].text_content().split(":")[1].split()[0]
            city = root.cssselect("table")[2][3].text_content().split(":")[1].split()[1]
        
        except IndexError: 
            plz = None
            city = None
        
        try:
            webpage = "http://fussball.de-vereine.de/link.php?id="+str(id)
            
        except IndexError: webpage = None
        
       # print url
        
        data = {'id' : id,
                'street' : street,
                'plz' : plz,
                'city' : city, 
                'name' : name,
                'webpage' : webpage
                } 

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def main():
    for id in range(6500):
        scrape_site(id)
        #time.sleep(5)

main()
    


