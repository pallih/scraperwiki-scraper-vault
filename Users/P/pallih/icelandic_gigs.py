import scraperwiki
import requests
import lxml.html
import urllib,urllib2
import simplejson

url = 'http://www.icelandmusic.is/live/gigs-abroad/'

# ESRI Locator service- for EU
# - EU addresses only
# - Unlimited geocoding using the method below (there are restrictions on batch geocoding: http://www.arcgis.com/home/item.html?id=41e621023bed4304b2a78e9d8b5ce67d )
def geocode(city,country):
    geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Address_EU/GeocodeServer/findAddressCandidates?Address=&City=%s&Postcode=&Country=%s&outFields=&outSR=&f=pjson' % (city,country)
    georeq = urllib2.Request(geocode_url)
    geo_response = urllib2.urlopen(georeq)
    try:
        geocode = simplejson.loads(geo_response.read())
        if len(geocode['candidates']):
            data_lat = geocode['candidates'][0]['location']['y']
            data_lng = geocode['candidates'][0]['location']['x']
            return {'lat':data_lat,'lng':data_lng}
    except:
        pass

response = requests.get(url)
root = lxml.html.fromstring(response.text)

months = root.xpath('//h2')
batch = []
for month in months:
    gigs = month.xpath('following-sibling::table/tr')
    for gig in gigs[1:]:
        record = {}
        record['band'] =  gig[0].text
        record['month'] =  gig[1].text
        record['date'] =  gig[2].text
        record['town'] =  gig[3].text
        record['country'] =  gig[4].text
        record['venue'] =  gig[5].text
        record['geo'] = geocode(record['town'].encode('utf-8'), record['country'].encode('utf-8'))
        batch.append(record)
print batch