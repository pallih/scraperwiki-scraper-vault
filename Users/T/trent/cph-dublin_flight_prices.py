###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from datetime import date
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'https://citosconnection.com/cek_jadwal.php?&adult=1&depDate=2012-07-20&ori=CGK,JAKARTA&des=BPN,BALIKPAPAN&__=1338521220068'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

divs = soup.findAll("div","fareCalDayDirect") 

for t in divs:
    travelDate = t.find("div","fareCalDate").contents[0]
    price = t.find("div","fareCalPrice").contents[0]
    directionDesc = t["id"]
    
    direction = ""
    if directionDesc.find("Out"):
        direction="Outbound"
    else:
        direction="Inbound" 

    record = {"direction":direction, "price" : price, "date" : travelDate.replace("&nbsp;","").lstrip().rstrip(), "run_date": date.today()}

    # save records to the datastore
    scraperwiki.datastore.save(["date","direction", "run_date"], record) ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from datetime import date
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'https://citosconnection.com/cek_jadwal.php?&adult=1&depDate=2012-07-20&ori=CGK,JAKARTA&des=BPN,BALIKPAPAN&__=1338521220068'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

divs = soup.findAll("div","fareCalDayDirect") 

for t in divs:
    travelDate = t.find("div","fareCalDate").contents[0]
    price = t.find("div","fareCalPrice").contents[0]
    directionDesc = t["id"]
    
    direction = ""
    if directionDesc.find("Out"):
        direction="Outbound"
    else:
        direction="Inbound" 

    record = {"direction":direction, "price" : price, "date" : travelDate.replace("&nbsp;","").lstrip().rstrip(), "run_date": date.today()}

    # save records to the datastore
    scraperwiki.datastore.save(["date","direction", "run_date"], record) 