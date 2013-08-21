###############################################################################
# Craigslist scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json

#prep regex for money
money = re.compile('\$[0-9]+')

# LOOK FOR:
# <h4 class="ban">Sat Jul 23</h4>

rooturl = "http://newyork.craigslist.org/aap/"
starturl = rooturl
# retrieve a page
while starturl != "":

    soup = BeautifulSoup( scraperwiki.scrape( starturl ) )
    starturllink = soup.find(text=re.compile("next 100 postings"))
    starturl = rooturl + starturllink.parent['href']
    print  "next target " + starturl
    for p in soup('p' , {"align":None} ):
        record ={}
        record['title'] = "No Title"
        record['link'] = "No Link"
        record['id']="noid"
        record['price']="Price Unlisted"
        record['location'] = "No Location"

        if p.font:
            # ditch the leading and trailing parentheses
            record['location'] =  re.subn(r"\(" , "" , re.subn(r"\)" , "" , p.font.text)[0] )[0]

        if p.a:
            if re.search( money, p.a.text ):
                amt = re.search(money, p.a.text ).group(0)
                record['price'] = amt
            
            record['title'] = p.a.text          

            if p.a['href']:
                record['link'] = p.a['href']     
                if re.search( r"/([\d]+)\.html" , p.a['href'] ):
                    record['id'] = re.subn( r"\.html","", re.subn( r"/" ,"", re.search( r"/([\d]+)\.html" , p.a['href'] ).group(0) )[0] )[0]
                    scraperwiki.sqlite.save( ["id"] , record )

            # print record['price'] + " " + record['title'] + " " + record['id']

        if len(soup.findAll('h4')) == 2:
            starturl = ""

