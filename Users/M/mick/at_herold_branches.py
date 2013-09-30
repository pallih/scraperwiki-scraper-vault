import scraperwiki
import lxml.html
import urllib
import urllib2
import simplejson

def getAllEntries(base_url, city, branch):
    url = base_url + "/" +city[0] +"/"+branch+"/"
    more_results = True
    page=1
    while more_results:
        if page==1:
            html = scraperwiki.scrape(url)
        else:
            current_page = root.find_class("current")
            if current_page:
                next_page = current_page[0].getparent().getnext()
                if next_page!=None:
                    p = next_page.text_content()
                    html = scraperwiki.scrape(url+str(page)+"/")
                else:
                    more_results = False
            else:
                    more_results = False
        page=page+1
    
    
        if more_results:           
            root = lxml.html.fromstring(html)
            results = root.find_class("result-wrap")
            for result in results:
                header = result.cssselect("h2")
                name = header[0].cssselect("a")
                
                div = result.find_class("addr")
                addr = div[0].cssselect("p")

                street_address = addr[0].text_content()
                try:
                    street_address = street_address[:street_address.index("/")]
                except:
                    print ""

                print street_address
                geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(street_address)+'&sensor=false&output=json'
                print geocode_url
                georeq = urllib2.Request(geocode_url)
                geo_response = urllib2.urlopen(georeq)
                geocode = simplejson.loads(geo_response.read())
                print geocode
                if geocode['status'] != 'ZERO_RESULTS':
                    data_lat = geocode['results'][0]['geometry']['location']['lat']
                    data_lng = geocode['results'][0]['geometry']['location']['lng']

                print data_lat
                print data_lng

                data = {
                    'city': city[1],
                    'branch': branch,
                    'business' : name[0].text_content(),
                    'address' : street_address,
                    'data_lat' : data_lat,
                    'data_lng' : data_lng
                }
                scraperwiki.sqlite.save(unique_keys=['business'], data=data)

def getTop10Branches():
    top10_branches = "http://www.herold.at/gelbe-seiten/branchen-az/"
    branches = []
    html = scraperwiki.scrape(top10_branches)
    root = lxml.html.fromstring(html)
    div = root.get_element_by_id("data_topsearch")

    for b in div.cssselect("ul")[0].cssselect("li"):
        branche = b.cssselect("a")[0].attrib['href']
        branche = branche[34:-1] #remove http://www.herold.at/gelbe-seiten/ and /
        branches.append(branche)
    return branches;

#---------------------------------------------------------------------------------------------------------------------------------------------------
#http://www.herold.at/gelbe-seiten/<bezirk>/<branche>/
base_url = "http://www.herold.at/gelbe-seiten/"

austrian_capitals=[["innsbruck-stadt","Innsbruck"], ["SqXmK_wien", "Wien"],["linz-stadt","Linz"], ["salzburg-stadt", "Salzburg"], ["graz-stadt", "Graz"], ["klagenfurt-stadt","Klagenfurt"], ["bregenz", "Bregenz"], ["13hSR_eisenstadt", "Eisenstadt"], ["SZwPC_sankt-pölten", "Sankt Pölten"]]
#austrian_capitals=[["13hSR_eisenstadt", "Eisenstadt"], ["SZwPC_sankt-pölten", "Sankt Pölten"]] 
#austrian_capitals=[["innsbruck-stadt","Innsbruck"],["SqXmK_wien", "Wien"]]

branches = getTop10Branches()
#branches = ["was_bars"]
for b in branches:
    print b

#city=austrian_capitals[0]
#branch = branches[0]

for b in branches:
    for city in austrian_capitals:
        print "Searching for ", b, " in ", city
        try:
            getAllEntries(base_url, city, b)
        except:
            print "Error during parsing. Skipping...."
import scraperwiki
import lxml.html
import urllib
import urllib2
import simplejson

def getAllEntries(base_url, city, branch):
    url = base_url + "/" +city[0] +"/"+branch+"/"
    more_results = True
    page=1
    while more_results:
        if page==1:
            html = scraperwiki.scrape(url)
        else:
            current_page = root.find_class("current")
            if current_page:
                next_page = current_page[0].getparent().getnext()
                if next_page!=None:
                    p = next_page.text_content()
                    html = scraperwiki.scrape(url+str(page)+"/")
                else:
                    more_results = False
            else:
                    more_results = False
        page=page+1
    
    
        if more_results:           
            root = lxml.html.fromstring(html)
            results = root.find_class("result-wrap")
            for result in results:
                header = result.cssselect("h2")
                name = header[0].cssselect("a")
                
                div = result.find_class("addr")
                addr = div[0].cssselect("p")

                street_address = addr[0].text_content()
                try:
                    street_address = street_address[:street_address.index("/")]
                except:
                    print ""

                print street_address
                geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(street_address)+'&sensor=false&output=json'
                print geocode_url
                georeq = urllib2.Request(geocode_url)
                geo_response = urllib2.urlopen(georeq)
                geocode = simplejson.loads(geo_response.read())
                print geocode
                if geocode['status'] != 'ZERO_RESULTS':
                    data_lat = geocode['results'][0]['geometry']['location']['lat']
                    data_lng = geocode['results'][0]['geometry']['location']['lng']

                print data_lat
                print data_lng

                data = {
                    'city': city[1],
                    'branch': branch,
                    'business' : name[0].text_content(),
                    'address' : street_address,
                    'data_lat' : data_lat,
                    'data_lng' : data_lng
                }
                scraperwiki.sqlite.save(unique_keys=['business'], data=data)

def getTop10Branches():
    top10_branches = "http://www.herold.at/gelbe-seiten/branchen-az/"
    branches = []
    html = scraperwiki.scrape(top10_branches)
    root = lxml.html.fromstring(html)
    div = root.get_element_by_id("data_topsearch")

    for b in div.cssselect("ul")[0].cssselect("li"):
        branche = b.cssselect("a")[0].attrib['href']
        branche = branche[34:-1] #remove http://www.herold.at/gelbe-seiten/ and /
        branches.append(branche)
    return branches;

#---------------------------------------------------------------------------------------------------------------------------------------------------
#http://www.herold.at/gelbe-seiten/<bezirk>/<branche>/
base_url = "http://www.herold.at/gelbe-seiten/"

austrian_capitals=[["innsbruck-stadt","Innsbruck"], ["SqXmK_wien", "Wien"],["linz-stadt","Linz"], ["salzburg-stadt", "Salzburg"], ["graz-stadt", "Graz"], ["klagenfurt-stadt","Klagenfurt"], ["bregenz", "Bregenz"], ["13hSR_eisenstadt", "Eisenstadt"], ["SZwPC_sankt-pölten", "Sankt Pölten"]]
#austrian_capitals=[["13hSR_eisenstadt", "Eisenstadt"], ["SZwPC_sankt-pölten", "Sankt Pölten"]] 
#austrian_capitals=[["innsbruck-stadt","Innsbruck"],["SqXmK_wien", "Wien"]]

branches = getTop10Branches()
#branches = ["was_bars"]
for b in branches:
    print b

#city=austrian_capitals[0]
#branch = branches[0]

for b in branches:
    for city in austrian_capitals:
        print "Searching for ", b, " in ", city
        try:
            getAllEntries(base_url, city, b)
        except:
            print "Error during parsing. Skipping...."
