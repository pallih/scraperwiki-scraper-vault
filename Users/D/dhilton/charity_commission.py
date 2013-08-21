###############################################################################
# Charity Commission scraper
# Author: Dan Hilton / @danhilton / daniel.hilton@gmail.com
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import urllib2


TRUSTEES_BASE_URL = "http://www.charitycommission.gov.uk/Showcharity/RegisterOfCharities/ContactAndTrustees.aspx?RegisteredCharityNumber="

# Utility function for extracting the names of trustees from a charity code.
def get_trustees(number):
    """
    Given a charity number, grab the trustees page, parse out the trustees and return as a list.
    """
    url = "".join([TRUSTEES_BASE_URL,number])
    corpus = scraperwiki.scrape(url)
    soup = BeautifulSoup(corpus)
    trustees = []
    #.ScrollingSelectionLeftColumn a    
    trustees_raw = soup.findAll('a', "LinkButton")
    for raw in trustees_raw:
        print raw.text
        print raw['href'].split('TID=')[1]
        person_id = raw['href'].split('TID=',1)[1]
        scraperwiki.datastore.save(['trustee']  , ({'trustee':raw.text,'person_id':person_id, 'charity_number':number}))


# First let's get a list of charity number's that are as uptodate as possible
# NOTE: you could just brute force this but this would take an _age_ to do.

charity_numbers = urllib2.urlopen("http://www.whatdotheyknow.com/request/30506/response/76765/attach/3/reg%20now.txt")
#charity_numbers = ['299758','1003530',] # if you want to test collisions

print charity_numbers.readline()


for number in charity_numbers.readlines():
    get_trustees(number)


