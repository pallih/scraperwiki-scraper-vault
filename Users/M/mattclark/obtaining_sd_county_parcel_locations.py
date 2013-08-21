import scraperwiki
import time
import csv
import urllib2
from BeautifulSoup import BeautifulSoup

#BEGINNING OF SCRAPER

# load parcels into list

data = scraperwiki.scrape("http://www.reportermattclark.com/SCRAPER/PNsWithNoLocation.csv")
parcels = csv.reader(data.splitlines())

# for each parcel in list

parcels.next()

for currentPN in list(parcels):

    # load url into a variable by slicing the parcel string
    url = "http://arcc.co.san-diego.ca.us/services/rollsearch/search.aspx?PB=" + currentPN[0][0:3] + "&PP=" + currentPN[0][3:6] + "&PN=" + currentPN[0][6:8] + "&PI=" + currentPN[0][8:10]

    # grab page
    #maybe do a try/except here or a loop
    try:
        page = scraperwiki.scrape(url)
    except:
        time.sleep(4)
        page = scraperwiki.scrape(url)

    # load the page into soup
    soup = BeautifulSoup(page)

    # load location into variable using soup
    location = soup.find('span', id="ctl00_ContentPlaceHolder1_lblLocation").string

    # put location into database
    if location is None:
        location = "No location listed"
    print  location + ", " + currentPN[0] + ", " + url
    scraperwiki.sqlite.save(unique_keys=["PN"], data={"PN":currentPN[0], "Address":location, "URL":url})

    # pause for 2 seconds
    time.sleep(4)

# done!


