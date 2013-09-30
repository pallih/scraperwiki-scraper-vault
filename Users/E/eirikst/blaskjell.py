#!/usr/bin/env python
# encoding: utf-8
import scraperwiki           
import urllib, urllib2, re, time
import urllib2
import socket
import simplejson   # for the geo-coder
from BeautifulSoup import BeautifulSoup
from time import strftime

# API-key I got for scraperwiki: ABQIAAAAgxlWnsfEg93hC1qDK2BFvhQWj4N4t6Xmv-CV_W48hf2y5mqxJRTcXxIPbJU4VsgoiOrAxZdN7z9pAg

#html = scraperwiki.scrape(url)
def checkURL(url, timeout=5, SSL=0):
    """Checks an url for a python version greater
    than 2.3.3.
    """

    defTimeOut=socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    found=1
    try:
        urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError,
        socket.error, socket.sslerror):
        found=0
        socket.setdefaulttimeout(defTimeOut)
    return found


def get_coordinates(geocode_adress):
    # a function to geocode a place.
    # geocoding from this tutorial: http://scraperwiki.com/scrapers/geocoding_examples/edit/
    geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(geocode_adress)+'&sensor=false&output=json'
           
    #print geocode_url
    georeq = urllib2.Request(geocode_url)
    geo_response = urllib2.urlopen(georeq)
    geocode = simplejson.loads(geo_response.read())
    #print geocode
        
    if geocode['status'] != 'OVER_QUERY_LIMIT' and geocode['status'] != 'ZERO_RESULTS':
        data_lat = geocode['results'][0]['geometry']['location']['lat']
        data_lng = geocode['results'][0]['geometry']['location']['lng']
        print "geocode worked"
    else:
        data_lat = ''
        data_lng = ''
        print "geocode failed"
    return data_lat, data_lng

def scrape_location(url):
    # a function to scrape a specific location from perma-link
    time.sleep(1) # hope that "IOError('socket error', timeout('timed out',))" is caused by stress. - so; relax!
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    a = soup.findAll('div', {"class":"blaaskjell-maalesteder-container"})
    for a in a:    
        # finding the data I'm looking for
        sted = a.find("h2").text.encode('utf-8')
        malested = a.find("p").text.encode('utf-8')
        malested = malested[11:] # slicing off "Målested: "
        try:
            dato = a.find("p", text=re.compile('.* uttatt dato.*'))
            dato = dato[19:]
        except:
            dato = ''
        melding = a.find("div")
        melding = melding.contents[3].p.text
        kommentar = a.find("div")
        kommentar= kommentar.contents[3].p.next.next.next.text 
        now = strftime("%d-%m-%Y %H:%M:%S") 
        #status = #1-4 kan, kan ikke, ingen melding, spis med måte
        
        #print data_lat
        #print data_lng
        #print "loc: %s" % (geocode_adress)
        #print "Sted: %s" % (sted)
        #print "Målested: %s" % (malested)
        #print "Dato: %s" % (dato)
        #print "Melding: %s" % (melding)
        #print "Kommentar: %s" % (kommentar)
        ## print "Status: %s" % (status)
        #print "URL: %s" % (url)
        data = {
          'Sted' : sted,
          'Malested' : malested,
          'Dato': dato,
          'Melding': melding,
          'Kommentar': kommentar,
          'URL': url,
          'scraped_date': now
        }
        #print data
        #print scraperwiki.sqlite.show_tables() 
        #save data (but not coordinates)
        scraperwiki.sqlite.save(unique_keys=['Malested'], data=data, table_name="skjell")
        # see if this location has coordinates in the other db table "location_data"
        old_rec = scraperwiki.sqlite.execute("select data_lat, data_lng from location_data WHERE Malested = '%s';" % (str(malested)))
        print old_rec
        try:
            if not old_rec['data'][0][0] or not old_rec['data'][0][1]:
                geocode_adress = " %s, %s, %s" % (malested, sted, "norway")
                data_lat, data_lng = get_coordinates(geocode_adress)
                location_data = {
                  'Malested' : malested,
                  'data_lat':data_lat,
                  'data_lng':data_lng
                }
                scraperwiki.sqlite.save(unique_keys=['Malested'], data=location_data, table_name="location_data")
                #scraperwiki.sqlite.save(['name', 'control_no'], data=record, table_name='us_georgia_corporate_entities')
        except IndexError:
                geocode_adress = " %s, %s, %s" % (malested, sted, "norway")
                data_lat, data_lng = get_coordinates(geocode_adress)
                location_data = {
                  'Malested' : malested,
                  'data_lat':data_lat,
                  'data_lng':data_lng
                }
                scraperwiki.sqlite.save(unique_keys=['Malested'], data=location_data, table_name="location_data")
        
#find urls of all locations listed here: på http://www.matportalen.no/verktoy/blaskjellvarsel/
url = 'http://www.matportalen.no/verktoy/blaskjellvarsel/' 
html = urllib.urlopen(url).read()
suppe = BeautifulSoup(html)
riktig_div = suppe.find('div', {'id':'widget'})

for link in riktig_div.findAll('a'):
     if link.has_key('href'):
         url = link['href']
         print url
         validity_test = checkURL(url)
         if validity_test ==1:
             scrape_location(url)


# select * from swdata order by years_in_school desc limit 10#!/usr/bin/env python
# encoding: utf-8
import scraperwiki           
import urllib, urllib2, re, time
import urllib2
import socket
import simplejson   # for the geo-coder
from BeautifulSoup import BeautifulSoup
from time import strftime

# API-key I got for scraperwiki: ABQIAAAAgxlWnsfEg93hC1qDK2BFvhQWj4N4t6Xmv-CV_W48hf2y5mqxJRTcXxIPbJU4VsgoiOrAxZdN7z9pAg

#html = scraperwiki.scrape(url)
def checkURL(url, timeout=5, SSL=0):
    """Checks an url for a python version greater
    than 2.3.3.
    """

    defTimeOut=socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    found=1
    try:
        urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError,
        socket.error, socket.sslerror):
        found=0
        socket.setdefaulttimeout(defTimeOut)
    return found


def get_coordinates(geocode_adress):
    # a function to geocode a place.
    # geocoding from this tutorial: http://scraperwiki.com/scrapers/geocoding_examples/edit/
    geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+urllib.quote_plus(geocode_adress)+'&sensor=false&output=json'
           
    #print geocode_url
    georeq = urllib2.Request(geocode_url)
    geo_response = urllib2.urlopen(georeq)
    geocode = simplejson.loads(geo_response.read())
    #print geocode
        
    if geocode['status'] != 'OVER_QUERY_LIMIT' and geocode['status'] != 'ZERO_RESULTS':
        data_lat = geocode['results'][0]['geometry']['location']['lat']
        data_lng = geocode['results'][0]['geometry']['location']['lng']
        print "geocode worked"
    else:
        data_lat = ''
        data_lng = ''
        print "geocode failed"
    return data_lat, data_lng

def scrape_location(url):
    # a function to scrape a specific location from perma-link
    time.sleep(1) # hope that "IOError('socket error', timeout('timed out',))" is caused by stress. - so; relax!
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    a = soup.findAll('div', {"class":"blaaskjell-maalesteder-container"})
    for a in a:    
        # finding the data I'm looking for
        sted = a.find("h2").text.encode('utf-8')
        malested = a.find("p").text.encode('utf-8')
        malested = malested[11:] # slicing off "Målested: "
        try:
            dato = a.find("p", text=re.compile('.* uttatt dato.*'))
            dato = dato[19:]
        except:
            dato = ''
        melding = a.find("div")
        melding = melding.contents[3].p.text
        kommentar = a.find("div")
        kommentar= kommentar.contents[3].p.next.next.next.text 
        now = strftime("%d-%m-%Y %H:%M:%S") 
        #status = #1-4 kan, kan ikke, ingen melding, spis med måte
        
        #print data_lat
        #print data_lng
        #print "loc: %s" % (geocode_adress)
        #print "Sted: %s" % (sted)
        #print "Målested: %s" % (malested)
        #print "Dato: %s" % (dato)
        #print "Melding: %s" % (melding)
        #print "Kommentar: %s" % (kommentar)
        ## print "Status: %s" % (status)
        #print "URL: %s" % (url)
        data = {
          'Sted' : sted,
          'Malested' : malested,
          'Dato': dato,
          'Melding': melding,
          'Kommentar': kommentar,
          'URL': url,
          'scraped_date': now
        }
        #print data
        #print scraperwiki.sqlite.show_tables() 
        #save data (but not coordinates)
        scraperwiki.sqlite.save(unique_keys=['Malested'], data=data, table_name="skjell")
        # see if this location has coordinates in the other db table "location_data"
        old_rec = scraperwiki.sqlite.execute("select data_lat, data_lng from location_data WHERE Malested = '%s';" % (str(malested)))
        print old_rec
        try:
            if not old_rec['data'][0][0] or not old_rec['data'][0][1]:
                geocode_adress = " %s, %s, %s" % (malested, sted, "norway")
                data_lat, data_lng = get_coordinates(geocode_adress)
                location_data = {
                  'Malested' : malested,
                  'data_lat':data_lat,
                  'data_lng':data_lng
                }
                scraperwiki.sqlite.save(unique_keys=['Malested'], data=location_data, table_name="location_data")
                #scraperwiki.sqlite.save(['name', 'control_no'], data=record, table_name='us_georgia_corporate_entities')
        except IndexError:
                geocode_adress = " %s, %s, %s" % (malested, sted, "norway")
                data_lat, data_lng = get_coordinates(geocode_adress)
                location_data = {
                  'Malested' : malested,
                  'data_lat':data_lat,
                  'data_lng':data_lng
                }
                scraperwiki.sqlite.save(unique_keys=['Malested'], data=location_data, table_name="location_data")
        
#find urls of all locations listed here: på http://www.matportalen.no/verktoy/blaskjellvarsel/
url = 'http://www.matportalen.no/verktoy/blaskjellvarsel/' 
html = urllib.urlopen(url).read()
suppe = BeautifulSoup(html)
riktig_div = suppe.find('div', {'id':'widget'})

for link in riktig_div.findAll('a'):
     if link.has_key('href'):
         url = link['href']
         print url
         validity_test = checkURL(url)
         if validity_test ==1:
             scrape_location(url)


# select * from swdata order by years_in_school desc limit 10