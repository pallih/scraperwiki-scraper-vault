import scraperwiki
import simplejson
import lxml.html
import time
import random
import urllib


class RacvFuelScraper:

    FUEL_TYPE = {
        'unleaded' : 2,
        'lpg' : 4,
        'diesel' : 3,
        'e10' : 6,
    }

    FEED_URL = 'http://www.racv.com.au/fuel/FuelFeed'
    PAGE_URL = 'http://www.racv.com.au/wps/wcm/connect/Internet/Primary/my+car/advice+_+information/fuel/petrol+prices'

    suburbs = []
    page_raw = ''
    json = {}

    def __init__(self):

        self.page_raw = scraperwiki.scrape(self.PAGE_URL)
        self.suburbs = self.getSuburbs()

        self.fillUp()

    def getSuburbs (self):

        # Get suburbs from RACV page

        print 'Getting suburbs'
        
        html = lxml.html.fromstring(self.page_raw)

        suburb_options = html.cssselect('#fuelSearch select[name=searchSuburb] option')
        exclude = ['0', '']
        suburbs = []
        
        for option in suburb_options:
            # Exclude rubbish
            if option.attrib['value'] in exclude:
                continue
            
            s = { 'label' : option.text, 'value' : option.attrib['value']}
            suburbs.append(s) # Good suburbs

        return suburbs
        
    def fillUp (self):

        RANDOM_WAIT_TIME = [1,5] # Min/Max for waiting random X seconds between requests

        print 'Getting fuel prices'

        for suburb in self.suburbs:

            # Wait a sec before request, because we don't want to get banned
            secs = random.randint(RANDOM_WAIT_TIME[0], RANDOM_WAIT_TIME[1])
            print 'Waiting {0} seconds'.format(secs)
            time.sleep(secs)

            self.json[suburb['value']] = self.getPrices(self.FUEL_TYPE['unleaded'], suburb['value'])

            data = simplejson.loads(self.json[suburb['value']])
            if data['ResultCode'] == 0:
                for station in data['Data']:
                    station['FuelType'] = self.FUEL_TYPE['unleaded']

                scraperwiki.sqlite.save(unique_keys=['SiteID'], data=data['Data'])
            else:
                print '- {code} - {msg}'.format(code=data['ResultCode'], msg=data['ResultMsg'])

        



    def getPrices (self, fuel_type, suburb):

        params = {
            'url' : 'localitysearch',
            'fuelType' : fuel_type,
            'Locality' : suburb,
        }

        param_str = urllib.urlencode(params)

        url = self.FEED_URL + '?' + param_str

        print 'Getting "{suburb}" with URL: {url}'.format(suburb=suburb, url=url)

        data = scraperwiki.scrape(url)

        data = data[ len('fuelString('):-2 ]

        return data
            

racv = RacvFuelScraper()import scraperwiki
import simplejson
import lxml.html
import time
import random
import urllib


class RacvFuelScraper:

    FUEL_TYPE = {
        'unleaded' : 2,
        'lpg' : 4,
        'diesel' : 3,
        'e10' : 6,
    }

    FEED_URL = 'http://www.racv.com.au/fuel/FuelFeed'
    PAGE_URL = 'http://www.racv.com.au/wps/wcm/connect/Internet/Primary/my+car/advice+_+information/fuel/petrol+prices'

    suburbs = []
    page_raw = ''
    json = {}

    def __init__(self):

        self.page_raw = scraperwiki.scrape(self.PAGE_URL)
        self.suburbs = self.getSuburbs()

        self.fillUp()

    def getSuburbs (self):

        # Get suburbs from RACV page

        print 'Getting suburbs'
        
        html = lxml.html.fromstring(self.page_raw)

        suburb_options = html.cssselect('#fuelSearch select[name=searchSuburb] option')
        exclude = ['0', '']
        suburbs = []
        
        for option in suburb_options:
            # Exclude rubbish
            if option.attrib['value'] in exclude:
                continue
            
            s = { 'label' : option.text, 'value' : option.attrib['value']}
            suburbs.append(s) # Good suburbs

        return suburbs
        
    def fillUp (self):

        RANDOM_WAIT_TIME = [1,5] # Min/Max for waiting random X seconds between requests

        print 'Getting fuel prices'

        for suburb in self.suburbs:

            # Wait a sec before request, because we don't want to get banned
            secs = random.randint(RANDOM_WAIT_TIME[0], RANDOM_WAIT_TIME[1])
            print 'Waiting {0} seconds'.format(secs)
            time.sleep(secs)

            self.json[suburb['value']] = self.getPrices(self.FUEL_TYPE['unleaded'], suburb['value'])

            data = simplejson.loads(self.json[suburb['value']])
            if data['ResultCode'] == 0:
                for station in data['Data']:
                    station['FuelType'] = self.FUEL_TYPE['unleaded']

                scraperwiki.sqlite.save(unique_keys=['SiteID'], data=data['Data'])
            else:
                print '- {code} - {msg}'.format(code=data['ResultCode'], msg=data['ResultMsg'])

        



    def getPrices (self, fuel_type, suburb):

        params = {
            'url' : 'localitysearch',
            'fuelType' : fuel_type,
            'Locality' : suburb,
        }

        param_str = urllib.urlencode(params)

        url = self.FEED_URL + '?' + param_str

        print 'Getting "{suburb}" with URL: {url}'.format(suburb=suburb, url=url)

        data = scraperwiki.scrape(url)

        data = data[ len('fuelString('):-2 ]

        return data
            

racv = RacvFuelScraper()