# -*- coding: utf-8 -*-

import scraperwiki
import mechanize
import cookielib
import urllib 
import urllib2 
import string 
import sys
import re
# BeautifulSoup for easier HTML parsing
from BeautifulSoup import BeautifulSoup

# Since we are going to fetch our data from a website, we have to behave like a browser
br = mechanize.Browser()

# Cookie Jar to store cookie
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False) # Please set this to True and read their site's robot.txt first before setting it back to False and proceeding

# Follows 1st refresh but no consequent refresh allawed to avoid browser hangs
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent: To behave like a browser, we will be needing to fake a user agent. For our program, I chose to push the webstatistics a little in favour of Firefox & Linux
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Ritual for RCI...
find_cruise_page = "http://bookings.royalcaribbean.co.uk/findacruise/search/vacationSearchResult/show.do?cruiseType=CO&pageType=AS&includeAdjascentPorts=Y&date=201300&date=201303&date=201304&date=201305&date=201306&date=201307&date=201308&date=201309&date=201310&port=&actionType=&portOfCall=&exp=true&price=&location=&promoType=&eventSource=date&duration=&dest=EUROP"
response = br.open(find_cruise_page)

# Load the links we stored after running DonRCI_all_links
scraperwiki.sqlite.attach("donmsc") 
cruise_links = {}
cruise_links = scraperwiki.sqlite.select("* from `RCI_Cruises_links`")
print "Number of cruises links detected from RCI find your cruise website:%d" % cruise_links[-1]['num']

# Get parameters after the most recent time the scraper is run and continue that scraping session OR reset the parameters and delete any old data if a new run is detected
if scraperwiki.sqlite.get_var('last_row_number') is not 0:
    i = scraperwiki.sqlite.get_var('last_row_number')
    start_again_at = scraperwiki.sqlite.get_var('last_terminate_at')
    print "Start again from %d where the last session was terminated..." % start_again_at        
else:
    i = 0
    start_again_at = 0
    print "Starting a new scraping session...."

# Go through all cruise links we found and get all the rates
cruises = {}
packages = {}
for c_link in cruise_links[start_again_at:-1]:
    try:
        i+=1
        cruises['id'] = i
        cruises['link'] = c_link['link']
        cruises['ports'] = c_link['ports_of_call']
        
        # Select relevant controls and set the criteria then submit - This is step 1 in their booking process
        br.open(c_link['link'])
        br.select_form("departureInfoForm")
        br["totalStaterooms"] = ['1']
        br["adultCount"] = ['3']
        br["childCount"] = ['1']
        #br["hasAir"] =
        #br["gateway"] =
        br.submit()
        
        # Start step 2 - choose category and get the price per guest per category
        step2 = br.geturl()
        response = br.open(step2)
        soup = BeautifulSoup(response.read())
        #print soup.prettify() 
        for title in soup.findAll('div', {'class':'yourCruiseModuleSection'}): 
            cruise_name = title('li')[1].text
            sail_date = title('li')[2].text
        cruises['name'] = cruise_name[7:len(cruise_name)]
        cruises['date'] = "".join(sail_date.split())
        for each in soup.findAll('script', {'type':'text/javascript'}):
            if (each is not None and "categories.push" in each.text): 
                some_script = each.text
                packages['cat'] = "".join(some_script[(some_script.find('categoryDisplayName')+23):(some_script.find('hasUpsell')-2)].split())
                packages['room_code'] = "".join(some_script[(some_script.find('code')+7):(some_script.find('occupancy')-2)].split())
                packages['rate'] = "".join(some_script[(some_script.find('rate1')-1):(some_script.find('rateTotal')-2)].split())
                packages['pack_id'] = str(i) + packages['room_code']
                scraperwiki.sqlite.save(['pack_id'], packages, "Meta Prices", 0)   
        scraperwiki.sqlite.save(['id'], cruises, "RCI_Cruises", 0)
        if (c_link['num']+1) == (cruise_links[-1]['num']):
            scraperwiki.sqlite.save_var('last_terminate_at', 0)
            scraperwiki.sqlite.save_var('last_row_number', 0)
            print "Scraping complete. Please check https://scraperwiki.com/docs/api?name=donrci_all_cruises#sqlite for result."
    except scraperwiki.CPUTimeExceededError:
        scraperwiki.sqlite.save_var('last_terminate_at', c_link['num']-1)
        scraperwiki.sqlite.save_var('last_row_number', i)
        raise
#http://www.royalcaribbean.com/booking/getDepartureInfo/checkAvailability.do?packageCode=NV07M193&shipCode=NV&sailDate=1130630&hasSenior=&hasMilitary=&hasFireandPolice=&state=

#http://bookings.royalcaribbean.co.uk/findacruise/cruiseDetails/itineraryAndPricing.do?hasSenior=&hasMilitary=&hasFireandPolice=&cruiseType=CO&state=&packageCode=NV07M193&date=201300_201303_201304_201305_201306_201307_201308_201309_201310&sailDate=1130630
# -*- coding: utf-8 -*-

import scraperwiki
import mechanize
import cookielib
import urllib 
import urllib2 
import string 
import sys
import re
# BeautifulSoup for easier HTML parsing
from BeautifulSoup import BeautifulSoup

# Since we are going to fetch our data from a website, we have to behave like a browser
br = mechanize.Browser()

# Cookie Jar to store cookie
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False) # Please set this to True and read their site's robot.txt first before setting it back to False and proceeding

# Follows 1st refresh but no consequent refresh allawed to avoid browser hangs
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent: To behave like a browser, we will be needing to fake a user agent. For our program, I chose to push the webstatistics a little in favour of Firefox & Linux
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Ritual for RCI...
find_cruise_page = "http://bookings.royalcaribbean.co.uk/findacruise/search/vacationSearchResult/show.do?cruiseType=CO&pageType=AS&includeAdjascentPorts=Y&date=201300&date=201303&date=201304&date=201305&date=201306&date=201307&date=201308&date=201309&date=201310&port=&actionType=&portOfCall=&exp=true&price=&location=&promoType=&eventSource=date&duration=&dest=EUROP"
response = br.open(find_cruise_page)

# Load the links we stored after running DonRCI_all_links
scraperwiki.sqlite.attach("donmsc") 
cruise_links = {}
cruise_links = scraperwiki.sqlite.select("* from `RCI_Cruises_links`")
print "Number of cruises links detected from RCI find your cruise website:%d" % cruise_links[-1]['num']

# Get parameters after the most recent time the scraper is run and continue that scraping session OR reset the parameters and delete any old data if a new run is detected
if scraperwiki.sqlite.get_var('last_row_number') is not 0:
    i = scraperwiki.sqlite.get_var('last_row_number')
    start_again_at = scraperwiki.sqlite.get_var('last_terminate_at')
    print "Start again from %d where the last session was terminated..." % start_again_at        
else:
    i = 0
    start_again_at = 0
    print "Starting a new scraping session...."

# Go through all cruise links we found and get all the rates
cruises = {}
packages = {}
for c_link in cruise_links[start_again_at:-1]:
    try:
        i+=1
        cruises['id'] = i
        cruises['link'] = c_link['link']
        cruises['ports'] = c_link['ports_of_call']
        
        # Select relevant controls and set the criteria then submit - This is step 1 in their booking process
        br.open(c_link['link'])
        br.select_form("departureInfoForm")
        br["totalStaterooms"] = ['1']
        br["adultCount"] = ['3']
        br["childCount"] = ['1']
        #br["hasAir"] =
        #br["gateway"] =
        br.submit()
        
        # Start step 2 - choose category and get the price per guest per category
        step2 = br.geturl()
        response = br.open(step2)
        soup = BeautifulSoup(response.read())
        #print soup.prettify() 
        for title in soup.findAll('div', {'class':'yourCruiseModuleSection'}): 
            cruise_name = title('li')[1].text
            sail_date = title('li')[2].text
        cruises['name'] = cruise_name[7:len(cruise_name)]
        cruises['date'] = "".join(sail_date.split())
        for each in soup.findAll('script', {'type':'text/javascript'}):
            if (each is not None and "categories.push" in each.text): 
                some_script = each.text
                packages['cat'] = "".join(some_script[(some_script.find('categoryDisplayName')+23):(some_script.find('hasUpsell')-2)].split())
                packages['room_code'] = "".join(some_script[(some_script.find('code')+7):(some_script.find('occupancy')-2)].split())
                packages['rate'] = "".join(some_script[(some_script.find('rate1')-1):(some_script.find('rateTotal')-2)].split())
                packages['pack_id'] = str(i) + packages['room_code']
                scraperwiki.sqlite.save(['pack_id'], packages, "Meta Prices", 0)   
        scraperwiki.sqlite.save(['id'], cruises, "RCI_Cruises", 0)
        if (c_link['num']+1) == (cruise_links[-1]['num']):
            scraperwiki.sqlite.save_var('last_terminate_at', 0)
            scraperwiki.sqlite.save_var('last_row_number', 0)
            print "Scraping complete. Please check https://scraperwiki.com/docs/api?name=donrci_all_cruises#sqlite for result."
    except scraperwiki.CPUTimeExceededError:
        scraperwiki.sqlite.save_var('last_terminate_at', c_link['num']-1)
        scraperwiki.sqlite.save_var('last_row_number', i)
        raise
#http://www.royalcaribbean.com/booking/getDepartureInfo/checkAvailability.do?packageCode=NV07M193&shipCode=NV&sailDate=1130630&hasSenior=&hasMilitary=&hasFireandPolice=&state=

#http://bookings.royalcaribbean.co.uk/findacruise/cruiseDetails/itineraryAndPricing.do?hasSenior=&hasMilitary=&hasFireandPolice=&cruiseType=CO&state=&packageCode=NV07M193&date=201300_201303_201304_201305_201306_201307_201308_201309_201310&sailDate=1130630
