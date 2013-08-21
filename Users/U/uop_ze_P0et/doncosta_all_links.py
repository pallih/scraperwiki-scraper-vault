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

# Follows 1st refresh but no consequent refresh allowed to avoid browser hangs
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent: To behave like a browser, we will be needing to fake a user agent. For our program, I chose to push the webstatistics a little in favour of Firefox & Linux
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Open the search page first, let's start small and find all European cruises only. This will also be the first page we start scraping as the search results start on the same page
month = 0
COS_links = {}
destinations = [ "western_mediterranean" , "eastern_mediterranean"  ]

# Open the search page first, let's start small and find all European cruises only. We will need to emulate the javascripts in the aspnet form to get the cruises.

i = 0
form_var = {}

for each_destination in destinations:
    for month in range (1,12):    
        cruise_page = "http://www.costacruises.co.uk/gb/cruises_list/%s-2013%02d.html" % (each_destination,month)
        form_var['link'] = cruise_page
        response = br.open(cruise_page)
        soup = BeautifulSoup(response.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
        
        # Get the parameters for javascripts emulation
        for each in soup.findAll('a'):
            java = each.get('href')
            if (java is not None and "btn_buttonBook" in java):
                i+=1
                form_var['id'] = i
                form_var['evnt_target'] = java[java.find('ct'):(java.find(',')-1)]
                form_var['evnt_arg'] = java[(java.find(',')+1):-1]
                scraperwiki.sqlite.save(['id'], form_var, "COS_form_var", 0)    
        
# Plug the parameters to javascripts so we can start submitting - This is step 1 in their booking process
for each_clink in form_var:
        br.open(form_var['link'])
        #br.select_form("aspnetForm")
        #br["__EVENTTARGET"] = form_var['evnt_target']
        #br["__EVENTARGUMENT"] = form_var['evnt_arg']
        #br.submit()
        
        # Start step 2    
        #step2 = br.geturl()
        #response = br.open(step2)
        #print step2
        #soup = BeautifulSoup(response.read())
        for form in br.forms():
            print "Form name:", form.name
            print form

# Now go through all the rest of the 11 pages of the Find-Your-Cruise and list all links to their cruises
#for num in range (1,10):
#    page = "http://bookings.royalcaribbean.co.uk/findacruise/search/vacationSearchResult/show.do?exp=true&pager.offset=%d0&grabSes=Y" % (num) 
#    response = br.open(page)
#    soup = BeautifulSoup(response.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
#    #print soup.prettify
#    for each in soup.findAll('a'):
#        link = each.get('href')
#        if (link is not None and "sailDate" in link):
#            package_code = link[(link.find('packageCode')+12):link.find('&date=')]
#            ship_code = package_code[0:2]
#            sail_date = link[(link.find('sailDate')+9):len(link)]
#            #cruise_links.append(link)
#            i+=1
#            ports = each.findParent('div', {'class':'cruiseInfo'}).find('p').text            
#            RCI_links['num'] = i
#            RCI_links['link'] = "http://www.royalcaribbean.com/booking/getDepartureInfo/checkAvailability.do?packageCode=%s&shipCode=%s&sailDate=%#s&hasSenior=&hasMilitary=&hasFireandPolice=&state=" % (package_code,ship_code,sail_date)
#            RCI_links['ports_of_call'] = "".join(ports.split())
#            scraperwiki.sqlite.save(['num'], RCI_links, "RCI_Cruises_links", 0)
#
# Go to DonRCI_all_cruises to start price scraping using the links we just found. Why don't we do this here in the same scraper you ask? Because of limited CPU time, that's why. Check this link for more info https://scraperwiki.com/docs/python/faq/#cpu_limit
