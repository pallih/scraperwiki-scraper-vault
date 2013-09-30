import scraperwiki
import lxml.html           
from urlparse import urljoin
import sys

process_existing = False

def process_airline(node) :
    
    print lxml.html.tostring(node)
        
    airline_code = node.cssselect("td")[1].text_content().strip()

    #print airline_code

    if not process_existing and exists(airline_code):        

        print "Not processing " + airline_code + ", already exists"

    else:

        try:
            
            
            airline_name = node.cssselect("td")[0].text_content().strip()
            three_digit_code = node.cssselect("td")[2].text_content().strip()
            icao_code = node.cssselect("td")[3].text_content().strip()
            country = node.cssselect("td")[4].text_content().strip()

            #city_name = get_data(root, 'City')
            #country_code = get_data(root, 'Country Abbrev.')
            #country_name = get_data(root, 'Country')
    
            print airline_code, airline_name, three_digit_code, icao_code, country
        
            airline_model = { "code" : airline_code, "name" : airline_name, "three_digit_code" : three_digit_code, "icao_code" : icao_code, "country" : country }
        
            scraperwiki.sqlite.save(unique_keys=["code"], table_name="airlines", data=airline_model)    
    
        except: # catch *all* exceptions
            
            e = sys.exc_info()[1]
            print "Errored " + str(e)
            
            try:
    
                error_model = { "code" : airline_code, "message" : str(e) }
                
                scraperwiki.sqlite.save(unique_keys=["url"], table_name="errors", data=error_model)    
            
            except: # catch *all* exceptions
                e = sys.exc_info()[1]
                print "Errored " + str(e)

def exists (code):
    
    print "Check if exists : " + code

    count = 0

    try:
        result = scraperwiki.sqlite.execute("select count(*) from airlines where code = ?", (code))
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

def scrape_airlinecodes() :

    print "Scraping Airline codes"

    page = "http://www.iata.org/membership/Pages/airline_members_list.aspx?All=true"
    
    print "Scraping page : " + page

    html = scraperwiki.scrape(page)
    
    root = lxml.html.fromstring(html)
    
    airlines = root.cssselect("#divRegion0 table.basictable-2 tr")

    #airlines = airlines[0:15]

    print len(airlines)

    for node in airlines:
    
        style = node.cssselect("[style]")
        title_row = node.cssselect("td:contains('Airline Name')")
        
        if (len(style) + len(title_row)) == 0:
            
            process_airline(node)
        
scrape_airlinecodes()import scraperwiki
import lxml.html           
from urlparse import urljoin
import sys

process_existing = False

def process_airline(node) :
    
    print lxml.html.tostring(node)
        
    airline_code = node.cssselect("td")[1].text_content().strip()

    #print airline_code

    if not process_existing and exists(airline_code):        

        print "Not processing " + airline_code + ", already exists"

    else:

        try:
            
            
            airline_name = node.cssselect("td")[0].text_content().strip()
            three_digit_code = node.cssselect("td")[2].text_content().strip()
            icao_code = node.cssselect("td")[3].text_content().strip()
            country = node.cssselect("td")[4].text_content().strip()

            #city_name = get_data(root, 'City')
            #country_code = get_data(root, 'Country Abbrev.')
            #country_name = get_data(root, 'Country')
    
            print airline_code, airline_name, three_digit_code, icao_code, country
        
            airline_model = { "code" : airline_code, "name" : airline_name, "three_digit_code" : three_digit_code, "icao_code" : icao_code, "country" : country }
        
            scraperwiki.sqlite.save(unique_keys=["code"], table_name="airlines", data=airline_model)    
    
        except: # catch *all* exceptions
            
            e = sys.exc_info()[1]
            print "Errored " + str(e)
            
            try:
    
                error_model = { "code" : airline_code, "message" : str(e) }
                
                scraperwiki.sqlite.save(unique_keys=["url"], table_name="errors", data=error_model)    
            
            except: # catch *all* exceptions
                e = sys.exc_info()[1]
                print "Errored " + str(e)

def exists (code):
    
    print "Check if exists : " + code

    count = 0

    try:
        result = scraperwiki.sqlite.execute("select count(*) from airlines where code = ?", (code))
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

def scrape_airlinecodes() :

    print "Scraping Airline codes"

    page = "http://www.iata.org/membership/Pages/airline_members_list.aspx?All=true"
    
    print "Scraping page : " + page

    html = scraperwiki.scrape(page)
    
    root = lxml.html.fromstring(html)
    
    airlines = root.cssselect("#divRegion0 table.basictable-2 tr")

    #airlines = airlines[0:15]

    print len(airlines)

    for node in airlines:
    
        style = node.cssselect("[style]")
        title_row = node.cssselect("td:contains('Airline Name')")
        
        if (len(style) + len(title_row)) == 0:
            
            process_airline(node)
        
scrape_airlinecodes()