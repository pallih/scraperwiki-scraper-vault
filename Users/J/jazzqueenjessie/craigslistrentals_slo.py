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

rooturl = "http://slo.craigslist.org/apa/"
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
        record['id']= "No ID"
        record['date'] = "no date"
        record['price']="Price Unlisted"
        record['location'] = "No Location"
        record['latitude'] = 0
        record['longitude'] = 0
        record['bedrooms'] = "Not listed"
        record['sqft'] = "Not listed"
        if p.font:
            # ditch the leading and trailing parentheses
            record['location'] =  re.subn(r"\(" , "" , re.subn(r"\)" , "" , p.font.text)[0] )[0]



        if p.a:
            #print "i'm here"
            if re.search( money, p.text ):
                amt = re.search(money, p.text ).group(0)
                record['price'] = amt

            #change this to find number of baths and square feet
            m = re.search(r"\dbr\b",p.text)
            
            if m:    
                record['bedrooms'] = m.group()
                print m.group()
            
            sq = re.search(r"\d+ft",p.text)
            if sq:
                record['sqft'] = sq.group()

            record['title'] = p.a.text          
            
            
            try:
                 if p['data-longitude']:
                    record['longitude'] = p['data-longitude']
                    record['latitude'] = p['data-latitude']
            except:
                print "No name"

            if p.a['href']:
                record['link'] = p.a['href']     
                if re.search( r"/([\d]+)\.html" , p.a['href'] ):
                    record['id'] = re.subn( r"\.html","", re.subn( r"/" ,"", re.search( r"/([\d]+)\.html" , p.a['href'] ).group(0) )[0] )[0]
                    scraperwiki.sqlite.save( ["id"] , record )

            # print record['price'] + " " + record['title'] + " " + record['id']

        if len(soup.findAll('h4')) == 2:
            starturl = ""

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

rooturl = "http://slo.craigslist.org/apa/"
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
        record['id']= "No ID"
        record['date'] = "no date"
        record['price']="Price Unlisted"
        record['location'] = "No Location"
        record['latitude'] = 0
        record['longitude'] = 0
        record['bedrooms'] = "Not listed"
        record['sqft'] = "Not listed"
        if p.font:
            # ditch the leading and trailing parentheses
            record['location'] =  re.subn(r"\(" , "" , re.subn(r"\)" , "" , p.font.text)[0] )[0]



        if p.a:
            #print "i'm here"
            if re.search( money, p.text ):
                amt = re.search(money, p.text ).group(0)
                record['price'] = amt

            #change this to find number of baths and square feet
            m = re.search(r"\dbr\b",p.text)
            
            if m:    
                record['bedrooms'] = m.group()
                print m.group()
            
            sq = re.search(r"\d+ft",p.text)
            if sq:
                record['sqft'] = sq.group()

            record['title'] = p.a.text          
            
            
            try:
                 if p['data-longitude']:
                    record['longitude'] = p['data-longitude']
                    record['latitude'] = p['data-latitude']
            except:
                print "No name"

            if p.a['href']:
                record['link'] = p.a['href']     
                if re.search( r"/([\d]+)\.html" , p.a['href'] ):
                    record['id'] = re.subn( r"\.html","", re.subn( r"/" ,"", re.search( r"/([\d]+)\.html" , p.a['href'] ).group(0) )[0] )[0]
                    scraperwiki.sqlite.save( ["id"] , record )

            # print record['price'] + " " + record['title'] + " " + record['id']

        if len(soup.findAll('h4')) == 2:
            starturl = ""

