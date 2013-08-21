###############################################################################
# Scrape official list of US Senators
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# Use the bioguide_id to form the image url
def imageUrlFromBioguideId(id):
    return 'http://bioguide.congress.gov/bioguide/photo/' + id[0] + '/' + id + '.jpg'

# retrieve the xml file containing US Senator info
starting_url = 'http://www.senate.gov/general/contact_information/senators_cfm.xml'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(xml)

# use BeautifulSoup to get all <member> elements
members = soup.findAll('member') 
for member in members:
    fields = member.findAll(True)
    record = {}
    for field in fields:
        record[field.name] = field.text
    record['image_url'] = imageUrlFromBioguideId(record['bioguide_id'])
    # save records to the datastore
    scraperwiki.datastore.save(["state", "class"], record) 
    