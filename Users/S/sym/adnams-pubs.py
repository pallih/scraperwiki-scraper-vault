import csv
import re
import urllib2

import BeautifulSoup

from scraperwiki import datastore
from scraperwiki import geo

class Outcodes():
    
    def __init__(self):
        self.download_outcodes()
    
    def download_outcodes(self):
        """
        Downloads a CSV file from http://www.freemaptools.com/ and puts it in 
        memory.
        """
        req = urllib2.urlopen('http://www.freemaptools.com/download/postcodes/postcodes.csv')
        self.outcodes = csv.DictReader(req)
    
    def next(self):
        return self.outcodes.next()

    def __iter__(self):
        return self

class Scrape():
    def __init__(self):
        pass
    
    def scrape(self, code):
        """
        Submits the form and returns the file like response object.
        """
        self.page = urllib2.urlopen("http://adnams.co.uk/beer/pub-finder?postcode=%s" % code)
    
    def parse(self):
        soup = BeautifulSoup.BeautifulSoup(self.page)
        results = []
        for result in soup.find('ul', id='pub-results').findAll('li'):
            pub = {}
            pub['name'] =  result.h3.string
            if not pub.get('name'):
                pub['name'] =  result.h3.a.string

            pub['address-line1'] = result.find('', {'class' : 'pub-address-line1'}).string
            pub['address-line2'] = result.find('', {'class' : 'pub-address-line2'}).string
            pub['address-line3'] = result.find('', {'class' : 'pub-address-line3'}).string
            pub['address-town'] = result.find('', {'class' : 'pub-address-town'}).string
            pub['address-county'] = result.find('', {'class' : 'pub-address-county'}).string
            pub['address-postcode'] = result.find('', {'class' : 'pub-address-postcode'}).string
            pub['telephone'] = result.find('', {'class' : 'pub-telephone'}).string
            pub['website'] = result.find('', {'class' : 'pub-website'}).string
    
            for k,v in pub.items():
                if not v:
                    del pub[k]
            results.append(pub)
        return results
            

scraper = Scrape()

for code in Outcodes():
    if code['outcode'][:2] == "IP" or code['outcode'][:2] == "NR":
        scraper.scrape(code['outcode'])
        results = scraper.parse()

        for pub in results:
            datastore.save(['name','address-postcode'], pub, latlng=geo.gb_postcode_to_latlng(pub['address-postcode']))














