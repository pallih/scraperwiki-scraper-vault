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

rooturl = "http://www.cpshomes.co.uk/lettings/properties/property_details.aspx?reference=P8152"
starturl = rooturl
# retrieve a page
while starturl != "":

    soup = BeautifulSoup( scraperwiki.scrape( starturl ) )
    starturl = rooturl #+ starturllink.parent['href']
    print  "next target " + starturl
    for p in soup('p' , {"align":None} ):
        record ={}
        record['postcode'] = "No title"
        record['address'] = "No address"
        record['bedCount']="No bed count"
        record['price']="No price"
        record['description'] = "No description"

        if p.font:
            # ditch the leading and trailing parentheses
            record['postcode'] =  re.search(^([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)$,starturl)[0]###############################################################################
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

rooturl = "http://www.cpshomes.co.uk/lettings/properties/property_details.aspx?reference=P8152"
starturl = rooturl
# retrieve a page
while starturl != "":

    soup = BeautifulSoup( scraperwiki.scrape( starturl ) )
    starturl = rooturl #+ starturllink.parent['href']
    print  "next target " + starturl
    for p in soup('p' , {"align":None} ):
        record ={}
        record['postcode'] = "No title"
        record['address'] = "No address"
        record['bedCount']="No bed count"
        record['price']="No price"
        record['description'] = "No description"

        if p.font:
            # ditch the leading and trailing parentheses
            record['postcode'] =  re.search(^([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)$,starturl)[0]