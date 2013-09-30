###############################################################################
# Basic scraper
###############################################################################

import re
import scraperwiki
import urlparse
from BeautifulSoup import BeautifulSoup



# retrieve a page
starting_url = 'http://www.crs.com/Find_A_CRS?state=AZ&country=US&rpp=2000&sort_by=last&with_photos=nope&state=AZ&rppfirst=350&rpplast=450&state=AZ&country=US&rpp=2000&sort_by=last&with_photos=yup&state=AZ&rppfirst=0&rpplast=1146&Next=Next+2000'







html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <span> tags
spans = soup.findAll('span')
for span in spans:
    span = str(span)
    
    ## get member id, open detail page
    x = re.search("/Display_Member\?rec=(\d+)", span, re.I)
    id = str(x.group(0))
    agent_url = urlparse.urljoin("http://www.crs.com", id)
    agent_info = scraperwiki.scrape(agent_url)
    agent_soup = BeautifulSoup(agent_info)
    #print agent_soup
    a = agent_soup.findAll('th', align="left")
    name = a[0].p.text

    
    agent = {}
    agent['data'] = a # save data in dictionary
    agent['name'] = name 
    #data["text"] = agent_text
    #data["latlng_lat"], data["latlng_lng"] = latlng
    # Choose unique keyname
    scraperwiki.datastore.save(unique_keys=['name'], data=agent)

###############################################################################
# Basic scraper
###############################################################################

import re
import scraperwiki
import urlparse
from BeautifulSoup import BeautifulSoup



# retrieve a page
starting_url = 'http://www.crs.com/Find_A_CRS?state=AZ&country=US&rpp=2000&sort_by=last&with_photos=nope&state=AZ&rppfirst=350&rpplast=450&state=AZ&country=US&rpp=2000&sort_by=last&with_photos=yup&state=AZ&rppfirst=0&rpplast=1146&Next=Next+2000'







html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <span> tags
spans = soup.findAll('span')
for span in spans:
    span = str(span)
    
    ## get member id, open detail page
    x = re.search("/Display_Member\?rec=(\d+)", span, re.I)
    id = str(x.group(0))
    agent_url = urlparse.urljoin("http://www.crs.com", id)
    agent_info = scraperwiki.scrape(agent_url)
    agent_soup = BeautifulSoup(agent_info)
    #print agent_soup
    a = agent_soup.findAll('th', align="left")
    name = a[0].p.text

    
    agent = {}
    agent['data'] = a # save data in dictionary
    agent['name'] = name 
    #data["text"] = agent_text
    #data["latlng_lat"], data["latlng_lng"] = latlng
    # Choose unique keyname
    scraperwiki.datastore.save(unique_keys=['name'], data=agent)

