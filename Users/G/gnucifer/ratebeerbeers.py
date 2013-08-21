import scraperwiki
import lxml.html
import re
import string
from urllib2 import URLError
from datetime import datetime
import time

from pprint import pprint

# TODO: first step get all urls only?

def beer_data(beer_root):

    data = []
    data.append(('name', beer_root.xpath('//h1')[0].text_content()))

    for a in beer_root.xpath("//a[@name='real average']"):
        average = a.text_content().strip()
        if average.startswith('WEIGHTED AVG: '):
            data.append(('weighted_average', average[14:]))
        elif average.startswith('MEAN: '):
            data.append(('real_average', average[6:]))

    
    #TODO: function for this operation, with logging if more than one found?
    result_etree = beer_root.xpath("//abbr[.='EST. CALORIES']/following-sibling::big")
    result = result_etree[0].text_content() if len(result_etree) else ''
    data.append(('calories', result))

    result_etree = beer_root.xpath("//abbr[.='ABV']/following-sibling::big")
    result = result_etree[0].text_content() if len(result_etree) else ''
    data.append(('abv', result))

    result_etree = beer_root.xpath("//abbr[.='IBU']/following-sibling::big")
    result = result_etree[0].text_content() if len(result_etree) else ''
    data.append(('ibu', result))

    result_etree = beer_root.xpath("//small[.='COMMERCIAL DESCRIPTION']/parent::div")
    result = result_etree[0].text_content().replace('COMMERCIAL DESCRIPTION', '', 1).strip() if len(result_etree) else ''
    data.append(('commercial_description', result))

    result_etree = beer_root.xpath("//div/text()[.='Style: ']/following-sibling::a[starts-with(@href, '/beerstyles/')]")
    result = result_etree[0].text_content() if len(result_etree) else ''
    data.append(('style', result))

    #return dict(map(lambda t, data))
    return dict([(k, v.strip()) for (k, v) in data])

def brewery_data(brewer_root):

    data = []
    data.append(('name', brewer_root.xpath("//h1")[0].text_content()))
        
    result_etree = brewer_root.xpath("//font[starts-with(.,'Type:')]")
    result = result_etree[0].text_content()[6:] if len(result_etree) else ''
    data.append(('type', result))

    result_etree = brewer_root.xpath("//a[starts-with(@href,'http://maps.google.com')]");
    result = result_etree[0].text_content() if len(result_etree) else ''
    data.append(('address', result))

    result_etree = brewer_root.xpath("//a[starts-with(@href,'tel:')]")
    result = result_etree[0].text_content() if len(result_etree) else ''
    data.append(('phone', result))

    #Extract homepage etc, no straigt forward way to do this
    #TODO: find acceptable way to get email
    #brewery_email = '';
        
    result_etree = brewer_root.xpath("//h1/../a")

    if len(result_etree):
        for brewery_link in result_etree:
            href = brewery_link.attrib['href']
            if href.startswith('http://www.facebook.com'):
                data.append(('facebook', href))
            elif href.startswith('http://www.twitter.com'):
                data.append(('twitter', href))
            else:
                data.append(('homepage', href))

    return dict([(k, v.strip()) for (k, v) in data])


def attempt_scrape(url, attempts=10, sleep_duration=10):
    #throw away non acii characters
    # for example: http://www.ratebeer.com/brewers/alpenfire-cider/11249/ contains a broken beer url
    filtered_url = url.encode('ascii', 'ignore') #filter(lambda x : x in string.printable, 
    html = None
    for attempt in range(attempts):
        try:
            html = scraperwiki.scrape(filtered_url)
        except URLError as e:
            print 'error'
            error = {
                'url' : url,
                'datetime' : datetime.today(),
                'type' : type(e),
                'reason' : e.reason,
                'args' : e.args
            }
            scraperwiki.sqlite.save(unique_keys=['url', 'datetime'], data=error, table_name="ratebeer_errors");
            # If temporary failure in name resolution
            if e.errno == -3:
                time.sleep(sleep_duration)
            else:
                break
        else:
            break
    return html
    


def scrape_brewery(url):

    result = scraperwiki.sqlite.execute("SELECT timestamp FROM ratebeer_breweries WHERE url = ?", [url])

    if len(result['data']):\
        #first row first column
        now = datetime.today()
        last_fetched = datetime.fromtimestamp(result['data'][0][0])

        if (now - last_fetched).days < 3:
            print 'skipping brewery: ' + url
            return


    beer_url_re = re.compile("^/beer/[^/]+/\d+/$")
    
    html = attempt_scrape(url)

    if(html is None):
        #TODO: Log error
        return

    brewery_root = lxml.html.fromstring(html)

    data = brewery_data(brewery_root)
    data['url'] = url
    data['filtered_url'] = url.encode('ascii', 'ignore')
    data['fetch_date'] = datetime.today()
    data['timestamp'] = time.time()

    scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name="ratebeer_breweries");
        
    for beer_a in brewery_root.xpath("//a[starts-with(@href, '/beer/') and not(starts-with(@href, '/beer/rate/'))]"):

        #some extra url filtering
        #replace with list comprehension for fun?
        if beer_url_re.search(beer_a.attrib['href']) is not None:
            beer_url = base_url + beer_a.attrib['href']
            scrape_beer(beer_url, url)
 
def scrape_beer(url, brewery_url):

    result = scraperwiki.sqlite.execute("SELECT timestamp FROM ratebeer_beers WHERE url = ?", [url])
 
    if len(result['data']):\
        #first row first column
        now = datetime.today()
        last_fetched = datetime.fromtimestamp(result['data'][0][0])

        if (now - last_fetched).days < 7:
            print 'skipping: ' + url
            return

    html = attempt_scrape(url)

    if(html is None):
        #TODO: Log error
        return

    beer_root = lxml.html.fromstring(html)

    data = beer_data(beer_root)
    data['url'] = url
    data['filtered_url'] = url.encode('ascii', 'ignore')
    data['brewery_url'] = brewery_url
    data['fetch_date'] = datetime.today()
    data['timestamp'] = time.time()

    scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name="ratebeer_beers");


#Things we want to extract:
# BEER:
# Name
# Dead/alive
# ABV
# Style
# Ratebeer url
# Brewery

##Primary key: Name + Brewery
#Primary key: ratebeer url

# BREWERY:
# Name (Using as primary key for now, might not be safe)
# Founded date
# Type
# Dead/alive
# Address (use reverse geocoding for more info like country etc since ratebeer address format varies)
# Coordinates (later from address)
# Ratebeer url
# Mail
# Twitter
# Facebook
# Homepage

#Primary key: Ratebeer url

#print scraperwiki.sqlite.show_tables()
#exit()

base_url = "http://www.ratebeer.com"

#scrape_brewery('http://www.ratebeer.com/brewers/alpenfire-cider/11249/')
#exit()


html = scraperwiki.scrape(base_url + "/BrowseBrewers.asp")
root = lxml.html.fromstring(html)


for a in root.cssselect(".beer a"):
    breweries_url = base_url + a.attrib['href']
    html = scraperwiki.scrape(breweries_url)
    brewers_root = lxml.html.fromstring(html);

    for brewer_a in brewers_root.cssselect(".beer .beerfoot a"):
        brewery_url = base_url + brewer_a.attrib['href']
        scrape_brewery(brewery_url)

    #pprint(dir(a))
    #pprint(a.__dict__, indent=2);