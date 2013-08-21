import scraperwiki
import BeautifulSoup
import HTMLParser
import datetime
import json


parser = HTMLParser.HTMLParser()

def getKMLFeed(url):
    print 'Scraping feed ' + url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    news = soup.findAll("placemark")
    pubdate = None

    for d in news:
        try:
            name = parser.unescape(d.find("name").getText())
            description = parser.unescape(d.find("description").getText())
            address = d.find("address").getText()
            data = {
                    "name":name,
                    "description":description,
                    "address":address,
                    "date":datetime.datetime.now(),
                    "source":url
                }
            scraperwiki.sqlite.save(unique_keys=['name', 'source'],data=data, table_name='placemarks')
        except Exception as e:
            print 'Oh dear, failed to scrape %s due to %s' % (url, e)

def hasLocation(address):
    for key in scraperwiki.sqlite.select("address from locations"):
        if key['address'] == address:
            return True;
    return False

def getLocations():
    for a in scraperwiki.sqlite.select("distinct address from placemarks"):
        address = a['address']

        if(address == ''):
            print 'No address for location'
            continue

        if(hasLocation(address)):
            # No need to get the location (already got it)
            print 'Already got ' + address
            continue

        try:
            addressEscaped = address.replace(' ', '%20')
            location = json.loads(scraperwiki.scrape('http://maps.googleapis.com/maps/api/geocode/json?address=' + addressEscaped  + '&sensor=false'))['results'][0]['geometry']['location']
            data = {
                    "address" : address,
                    "latitude" : location['lat'],
                    "longitude" : location['lng']
                }
            print 'Saving location for ' + address 
            scraperwiki.sqlite.save(unique_keys=['address'],data=data, table_name='locations')
        except Exception as e:
            print 'Oh dear, failed to scrape %s due to %s' % (address, e)

def scrapeFeeds():
    getKMLFeed('http://www.cbsnews.com/common/includes/google/cbsnewsfiles.kml')
    
scrapeFeeds()
getLocations()import scraperwiki
import BeautifulSoup
import HTMLParser
import datetime
import json


parser = HTMLParser.HTMLParser()

def getKMLFeed(url):
    print 'Scraping feed ' + url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    news = soup.findAll("placemark")
    pubdate = None

    for d in news:
        try:
            name = parser.unescape(d.find("name").getText())
            description = parser.unescape(d.find("description").getText())
            address = d.find("address").getText()
            data = {
                    "name":name,
                    "description":description,
                    "address":address,
                    "date":datetime.datetime.now(),
                    "source":url
                }
            scraperwiki.sqlite.save(unique_keys=['name', 'source'],data=data, table_name='placemarks')
        except Exception as e:
            print 'Oh dear, failed to scrape %s due to %s' % (url, e)

def hasLocation(address):
    for key in scraperwiki.sqlite.select("address from locations"):
        if key['address'] == address:
            return True;
    return False

def getLocations():
    for a in scraperwiki.sqlite.select("distinct address from placemarks"):
        address = a['address']

        if(address == ''):
            print 'No address for location'
            continue

        if(hasLocation(address)):
            # No need to get the location (already got it)
            print 'Already got ' + address
            continue

        try:
            addressEscaped = address.replace(' ', '%20')
            location = json.loads(scraperwiki.scrape('http://maps.googleapis.com/maps/api/geocode/json?address=' + addressEscaped  + '&sensor=false'))['results'][0]['geometry']['location']
            data = {
                    "address" : address,
                    "latitude" : location['lat'],
                    "longitude" : location['lng']
                }
            print 'Saving location for ' + address 
            scraperwiki.sqlite.save(unique_keys=['address'],data=data, table_name='locations')
        except Exception as e:
            print 'Oh dear, failed to scrape %s due to %s' % (address, e)

def scrapeFeeds():
    getKMLFeed('http://www.cbsnews.com/common/includes/google/cbsnewsfiles.kml')
    
scrapeFeeds()
getLocations()