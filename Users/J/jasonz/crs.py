import re
import scraperwiki
import urlparse
from BeautifulSoup import BeautifulSoup



# retrieve a page
starting_url = 'http://www.crs.com/Find_A_CRS?findem=1&city=Boulder&state=CO&zip=&country=US&geo=&last=&company=&spec=ALL&email=&lang=ALL&designation=ALL&cert=ALL&with_photos=yup&rpp=25&sort_by=last&Input=Begin+Search'
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
    agent = scraperwiki.scrape(agent_url)
    agent_soup = BeautifulSoup(agent)
    #print agent_soup
    a = agent_soup.findAll('th', align="left")
    name = a[0].p.text



    
    data = {'name': name} # save data in dictionary
    data["text"] = str(a)
    #data["latlng_lat"], data["latlng_lng"] = latlng
    # Choose unique keyname
    scraperwiki.datastore.save(unique_keys=['name'], data=data)
