import scraperwiki
import lxml.html
from datetime import datetime

def fetch_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

try:
    scraperwiki.sqlite.execute("drop table gigs")
except:
    pass

scraperwiki.sqlite.execute("create table gigs (day date, title string, link string, address string, phonenumber string, lng int, lat int, postcode string)")

url = "http://www.yorkgigguide.com/december.html"

root = fetch_html(url)
d = None
for gig in root.get_element_by_id('pageContent')[:4]:
    
    artist = description = time = phonenumber = postcode = venue = address = lat = lng = link = None
    if gig.find_class('dateBanner'):
        d = gig.find_class('dateBanner')[0].text.replace('th', '')
        #d = d.replace('st', '')
        #d = d.replace('nd', '')
        d = datetime.strptime(d, '%A %d %B %Y')
    if gig.find_class('artiste'):
        artist = gig.find_class('artiste')[0].text
    if gig.find_class('blurb'):
        description = gig.find_class('blurb')[0].text
    if gig.find_class('time'):
        time = gig.find_class('time')[0].text
    if gig.find_class('venue'):
        #print gig.find_class('venue')[0].text
        venue_details = gig.find_class('venue')[0].text.split('Tel:')

        venue = venue_details[0]
        if len(venue_details) > 1:
            phonenumber = venue_details[1]
    try:
        postcode = scraperwiki.geo.extract_gb_postcode(venue_details)
        lat, lng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    except:
        pass

    # day date, title string, link string, address string, phonenumber string, lng int, lat int, postcode string
    scraperwiki.sqlite.execute('insert into gigs values (?, ?, ?, ?, ?, ?, ?, ?)', (d, description, 
                                link, address, phonenumber, lng, lat, postcode))
    scraperwiki.sqlite.commit()

    
