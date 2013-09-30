import scraperwiki
import urllib
import json
from bs4 import BeautifulSoup
from time import sleep

def geocode(postcode):
    url = 'http://mapit.mysociety.org/postcode/%s.json' % postcode
    result = urllib.urlopen(url).read()
    return json.loads(result)

def scrape():
    url = 'http://search.camden.gov.uk/search?site=lra&client=lra&output=xml_no_dtd&entqr=0&access=p&getfields=*&filter=0&q=inmeta%3ASTATUS&sort=date%3AD%3AS%3Ad1&num=1000&start=0&_=1368176037942'
    xml = urllib.urlopen(url).read()
    doc = BeautifulSoup(xml)

    licenses = []

    #get each license
    for r in doc.find_all('r'):
        license = {}
        license['url'] = r.ue.text
        license['reference'] = r.t.text.split('#')[1]
        for mt in r.find_all('mt'):
            license[mt['n'].lower()] = mt['v']

        licenses.append(license)

    #try and geocode each license
    for license in licenses:
        sleep(0.3)
        try:
            location = geocode(license['postcode'])
            # license.easting =
            license['northing'] = location['northing']
            license['easting'] = location['easting']
            license['wgs84_lat'] = location['wgs84_lat']
            license['wgs84_lon'] = location['wgs84_lon']
        except:
            print "Failed to geocode"

    #save
    for license in licenses:
        scraperwiki.sqlite.save(unique_keys=["url"], data=license)


#run
scrape()
import scraperwiki
import urllib
import json
from bs4 import BeautifulSoup
from time import sleep

def geocode(postcode):
    url = 'http://mapit.mysociety.org/postcode/%s.json' % postcode
    result = urllib.urlopen(url).read()
    return json.loads(result)

def scrape():
    url = 'http://search.camden.gov.uk/search?site=lra&client=lra&output=xml_no_dtd&entqr=0&access=p&getfields=*&filter=0&q=inmeta%3ASTATUS&sort=date%3AD%3AS%3Ad1&num=1000&start=0&_=1368176037942'
    xml = urllib.urlopen(url).read()
    doc = BeautifulSoup(xml)

    licenses = []

    #get each license
    for r in doc.find_all('r'):
        license = {}
        license['url'] = r.ue.text
        license['reference'] = r.t.text.split('#')[1]
        for mt in r.find_all('mt'):
            license[mt['n'].lower()] = mt['v']

        licenses.append(license)

    #try and geocode each license
    for license in licenses:
        sleep(0.3)
        try:
            location = geocode(license['postcode'])
            # license.easting =
            license['northing'] = location['northing']
            license['easting'] = location['easting']
            license['wgs84_lat'] = location['wgs84_lat']
            license['wgs84_lon'] = location['wgs84_lon']
        except:
            print "Failed to geocode"

    #save
    for license in licenses:
        scraperwiki.sqlite.save(unique_keys=["url"], data=license)


#run
scrape()
