import scraperwiki
import lxml.html           
from urlparse import urljoin
import sys

process_existing = False

def get_data(node, field):

    return node.cssselect("label.detail:contains('" + field + "')")[0].getnext().text_content()[1:].strip().strip(" (?)")

def scrape_airport(url) :

    try:

        #Clean strange characters from URL
        url = url.replace('\xe3', 'ã')
    
        if not process_existing and airport_exists(url):        
    
            print "Not Scraping " + url + ", already exists"
    
        else:
    
            print "Scraping " + url
    
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            
            airport_code = get_data(root, 'Airport Code')
            airport_name = get_data(root, 'Airport Name')
            city_name = get_data(root, 'City')
            country_code = get_data(root, 'Country Abbrev.')
            country_name = get_data(root, 'Country')
    
            print airport_code, airport_name, city_name, country_code, country_name
        
            airport_model = { "url" : url, "code" : airport_code, "name" : airport_name, "city" : city_name, "country_code" : country_code, "country_name" : country_name }
        
            scraperwiki.sqlite.save(unique_keys=["url"], table_name="airports", data=airport_model)    

    except: # catch *all* exceptions
        
        e = sys.exc_info()[1]
        print "Errored " + str(e)
        
        try:

            error_model = { "url" : url.decode('utf-8', 'replace'), "message" : str(e) }
            
            scraperwiki.sqlite.save(unique_keys=["url"], table_name="errors", data=error_model)    
        
        except: # catch *all* exceptions
            e = sys.exc_info()[1]
            print "Errored " + str(e)

def airport_exists (url):
    
    print "airport_exists : " + url

    count = 0

    try:
        result = scraperwiki.sqlite.execute("select count(*) from airports where url = ?", (url))
        count = int(result["data"][0][0])  

        #print "result : " + str(result)
        #print "result['data'] : " + str(result["data"])
        #print "result['data'][0] : " + str(result["data"][0])
        #print "result['data'][0][0] : " + str(result["data"][0][0])
    
        #print "result is list : " + str(type(result) is list)
        #print "result['data'] is list : " + str(type(result["data"]) is list)
        #print "result['data'][0][0] is list : " + str(type(result["data"][0][0]) is list)
        
        #print "Count : " + str(count)

    except scraperwiki.sqlite.SqliteError, e:
        print "Unexpected error:" + str(e)

    return count > 0

def scrape_airports_az() :
    print "Scraping airports a-z"
    
    
    #For a-z - 97, 122
    for i in range(ord('s'), ord('z') + 1):

        #print i , chr(i) 
        page = "http://www.world-airport-codes.com/alphabetical/country-name/" + chr(i) + ".html"
        
        print "Scraping page : " + page

        html = scraperwiki.scrape(page)
        
        root = lxml.html.fromstring(html)
        
        airports = root.cssselect("tr.one, tr.two")

        #airports = airports[0:2]

        for airport in airports:
        
            country_name = airport.cssselect("td")[0].text_content()
            airport_name = airport.cssselect("td")[2].text_content()
            airport_url_relative = airport.cssselect("td")[2].cssselect("a")[0].attrib.get('href')
    
            airport_url = urljoin(page, airport_url_relative)
        
            print country_name, airport_name, airport_url

            scrape_airport(airport_url)
        
scrape_airports_az()
#scrape_airport("http://www.world-airport-codes.com/brazil/gale\xe3o\x96antonio-carlos-jobim-international-airport-6296.html")import scraperwiki
import lxml.html           
from urlparse import urljoin
import sys

process_existing = False

def get_data(node, field):

    return node.cssselect("label.detail:contains('" + field + "')")[0].getnext().text_content()[1:].strip().strip(" (?)")

def scrape_airport(url) :

    try:

        #Clean strange characters from URL
        url = url.replace('\xe3', 'ã')
    
        if not process_existing and airport_exists(url):        
    
            print "Not Scraping " + url + ", already exists"
    
        else:
    
            print "Scraping " + url
    
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            
            airport_code = get_data(root, 'Airport Code')
            airport_name = get_data(root, 'Airport Name')
            city_name = get_data(root, 'City')
            country_code = get_data(root, 'Country Abbrev.')
            country_name = get_data(root, 'Country')
    
            print airport_code, airport_name, city_name, country_code, country_name
        
            airport_model = { "url" : url, "code" : airport_code, "name" : airport_name, "city" : city_name, "country_code" : country_code, "country_name" : country_name }
        
            scraperwiki.sqlite.save(unique_keys=["url"], table_name="airports", data=airport_model)    

    except: # catch *all* exceptions
        
        e = sys.exc_info()[1]
        print "Errored " + str(e)
        
        try:

            error_model = { "url" : url.decode('utf-8', 'replace'), "message" : str(e) }
            
            scraperwiki.sqlite.save(unique_keys=["url"], table_name="errors", data=error_model)    
        
        except: # catch *all* exceptions
            e = sys.exc_info()[1]
            print "Errored " + str(e)

def airport_exists (url):
    
    print "airport_exists : " + url

    count = 0

    try:
        result = scraperwiki.sqlite.execute("select count(*) from airports where url = ?", (url))
        count = int(result["data"][0][0])  

        #print "result : " + str(result)
        #print "result['data'] : " + str(result["data"])
        #print "result['data'][0] : " + str(result["data"][0])
        #print "result['data'][0][0] : " + str(result["data"][0][0])
    
        #print "result is list : " + str(type(result) is list)
        #print "result['data'] is list : " + str(type(result["data"]) is list)
        #print "result['data'][0][0] is list : " + str(type(result["data"][0][0]) is list)
        
        #print "Count : " + str(count)

    except scraperwiki.sqlite.SqliteError, e:
        print "Unexpected error:" + str(e)

    return count > 0

def scrape_airports_az() :
    print "Scraping airports a-z"
    
    
    #For a-z - 97, 122
    for i in range(ord('s'), ord('z') + 1):

        #print i , chr(i) 
        page = "http://www.world-airport-codes.com/alphabetical/country-name/" + chr(i) + ".html"
        
        print "Scraping page : " + page

        html = scraperwiki.scrape(page)
        
        root = lxml.html.fromstring(html)
        
        airports = root.cssselect("tr.one, tr.two")

        #airports = airports[0:2]

        for airport in airports:
        
            country_name = airport.cssselect("td")[0].text_content()
            airport_name = airport.cssselect("td")[2].text_content()
            airport_url_relative = airport.cssselect("td")[2].cssselect("a")[0].attrib.get('href')
    
            airport_url = urljoin(page, airport_url_relative)
        
            print country_name, airport_name, airport_url

            scrape_airport(airport_url)
        
scrape_airports_az()
#scrape_airport("http://www.world-airport-codes.com/brazil/gale\xe3o\x96antonio-carlos-jobim-international-airport-6296.html")