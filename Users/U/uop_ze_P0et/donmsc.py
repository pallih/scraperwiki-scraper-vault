# -*- coding: utf-8 -*-

import scraperwiki
import mechanize
import cookielib
import urllib 
import urllib2 
import string 
import sys
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

# Open the search page first, let's start small and find all European cruises only. This will also be the first page we start scraping as the search results start on the same page
i = 0
#cruise_links = []
RCI_links = {}
find_cruise_page = "http://bookings.royalcaribbean.co.uk/findacruise/search/vacationSearchResult/show.do?cruiseType=CO&pageType=AS&includeAdjascentPorts=Y&date=201300&date=201303&date=201304&date=201305&date=201306&date=201307&date=201308&date=201309&date=201310&port=&actionType=&portOfCall=&exp=true&price=&location=&promoType=&eventSource=date&duration=&dest=EUROP"
response = br.open(find_cruise_page)
soup = BeautifulSoup(response.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
for each in soup.findAll('a'):
    link = each.get('href')
    if (link is not None and "sailDate" in link):
        package_code = link[(link.find('packageCode')+12):link.find('&date=')]
        ship_code = package_code[0:2]
        sail_date = link[(link.find('sailDate')+9):len(link)]
        #cruise_links.append(link)
        i+=1
        ports = each.findParent('div', {'class':'cruiseInfo'}).find('p').text            
        RCI_links['num'] = i
        RCI_links['link'] = "http://www.royalcaribbean.com/booking/getDepartureInfo/checkAvailability.do?packageCode=%s&shipCode=%s&sailDate=%s&hasSenior=&hasMilitary=&hasFireandPolice=&state=" % (package_code,ship_code,sail_date)
        RCI_links['ports_of_call'] = "".join(ports.split())
        scraperwiki.sqlite.save(['num'], RCI_links, "RCI_Cruises_links", 0)
    

# Now go through all the rest of the 11 pages of the Find-Your-Cruise and list all links to their cruises
for num in range (1,10):
    page = "http://bookings.royalcaribbean.co.uk/findacruise/search/vacationSearchResult/show.do?exp=true&pager.offset=%d0&grabSes=Y" % (num) 
    response = br.open(page)
    soup = BeautifulSoup(response.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
    #print soup.prettify
    for each in soup.findAll('a'):
        link = each.get('href')
        if (link is not None and "sailDate" in link):
            package_code = link[(link.find('packageCode')+12):link.find('&date=')]
            ship_code = package_code[0:2]
            sail_date = link[(link.find('sailDate')+9):len(link)]
            #cruise_links.append(link)
            i+=1
            ports = each.findParent('div', {'class':'cruiseInfo'}).find('p').text            
            RCI_links['num'] = i
            RCI_links['link'] = "http://www.royalcaribbean.com/booking/getDepartureInfo/checkAvailability.do?packageCode=%s&shipCode=%s&sailDate=%s&hasSenior=&hasMilitary=&hasFireandPolice=&state=" % (package_code,ship_code,sail_date)
            RCI_links['ports_of_call'] = "".join(ports.split())
            scraperwiki.sqlite.save(['num'], RCI_links, "RCI_Cruises_links", 0)

# Go to DonRCI_all_cruises to start price scraping using the links we just found. Why don't we do this here in the same scraper you ask? Because of limited CPU time, that's why. Check this link for more info https://scraperwiki.com/docs/python/faq/#cpu_limit
