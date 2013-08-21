import scraperwiki

from scraperwiki import datastore
from BeautifulSoup import BeautifulStoneSoup

import urllib2
import urllib

# this looks like it accesses a single page database dump of the whole set
# without a view on a shorter version of the page it's hard to tell which fields are actually used.

url = "http://www.nhs.uk/NHSCWS/Services/ServicesSearch.aspx?user=Hackday.2&pwd=WOdaJaGc&type=5&PageSize=200000&"

xml = scraperwiki.scrape("http://www.nhs.uk/NHSCWS/Services/ServicesSearch.aspx?user=Hackday.2&pwd=WOdaJaGc&type=5&q=%20&")
page = BeautifulStoneSoup(xml)
for location in page.findAll('location'):
    postcode = location.value.string.strip().split(',')[-1][:-1].strip()
    print postcode
    l = urllib.urlencode({'q': postcode})
    results = scraperwiki.scrape(url+l)
    services = BeautifulStoneSoup(results, selfClosingTags=[
        'coords',
        'code1',
        'code2',
        'address1',
        'address2',
        'address3',
        'address4',
        ])
    for service in services.findAll('service'):
        data = {}
        
        data['code1'] = service.code1.string

        data['code2'] = service.code2.string
        
        data['name'] = service.find('name').string
        data['address1'] = service.address1.string
        data['address2'] = service.address2.string
        data['address3'] = service.address3.string
        data['address4'] = service.address4.string
        data['address5'] = service.address5.string
        data['postcode'] = service.postcode.string

        data['telephone'] = service.telephone.string
        data['website'] = service.website.string

        data['northing'] = service.northing.string
        data['easting'] = service.easting.string
        data['latitude'] = service.latitude.string
        data['longitude'] = service.longitude.string
        data['coords'] = service.coords
        
        data['hasaande'] = service.hasaande.string
        data['category'] = service.category.string
        data['organisationcommentcount'] = service.organisationcommentcount.string
        data['providerprofilepageurl'] = service.providerprofilepageurl.string

        latlng = (float(data['latitude']), float(data['longitude']))
        datastore.save(unique_keys=['name'], data=data, latlng=latlng)

