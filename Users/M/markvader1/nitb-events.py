# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events"

# searchpathfor = "MeatLoaf"


def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0

#    while root1 is not None:
#        print "*** root ***", r
#        FindContentsRecurse(root1)
#        root1 = root1.getnext()
#        r += 1

    # place your cssselection case here and extract the values
    for tr in root.cssselect('table.eventslist tr'):
        record = {}

#        print list(tr), lxml.etree.tostring(tr)

        date_range = tr[0].text.split('\r\n\t\t\t- ')
        if len(date_range) == 2:
            record['date_to'] = date_range[1].strip()

        record['date_from'] = date_range[0].strip()
        record['subjects'] = tr[1][0].text.split(",") # TODO needs further cleanup to remove trailing \r\n (perhaps using rstrip() ?
        record['location'] = tr[1][1].tail
        record['event_name'] = tr[2][0][0].text
        event_url = "http://www.discovernorthernireland.com" + tr[2][0].attrib['href']
        record['event_url'] = event_url
        print record
        scraperwiki.datastore.save(["NITB_Events"], record)


# TODO       Also parse each event_url and get the pricing information from div.tabContainer on those pages also
#
#        event_root = lxml.html.parse(event_url).getroot()
#        for info_tab in event_root.cssselect('div.tabContainer div.narrativedetails h3'):
#            
#            if  event_root.cssselect('div.tabContainer div.narrativedetails h3').text == "Price:":
#                print event_url, event_root.cssselect('div.tabContainer div.narrativedetails')[0].text
#
#            print event_url, lxml.etree.tostring(event_price)

                

       
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events"

# searchpathfor = "MeatLoaf"


def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0

#    while root1 is not None:
#        print "*** root ***", r
#        FindContentsRecurse(root1)
#        root1 = root1.getnext()
#        r += 1

    # place your cssselection case here and extract the values
    for tr in root.cssselect('table.eventslist tr'):
        record = {}

#        print list(tr), lxml.etree.tostring(tr)

        date_range = tr[0].text.split('\r\n\t\t\t- ')
        if len(date_range) == 2:
            record['date_to'] = date_range[1].strip()

        record['date_from'] = date_range[0].strip()
        record['subjects'] = tr[1][0].text.split(",") # TODO needs further cleanup to remove trailing \r\n (perhaps using rstrip() ?
        record['location'] = tr[1][1].tail
        record['event_name'] = tr[2][0][0].text
        event_url = "http://www.discovernorthernireland.com" + tr[2][0].attrib['href']
        record['event_url'] = event_url
        print record
        scraperwiki.datastore.save(["NITB_Events"], record)


# TODO       Also parse each event_url and get the pricing information from div.tabContainer on those pages also
#
#        event_root = lxml.html.parse(event_url).getroot()
#        for info_tab in event_root.cssselect('div.tabContainer div.narrativedetails h3'):
#            
#            if  event_root.cssselect('div.tabContainer div.narrativedetails h3').text == "Price:":
#                print event_url, event_root.cssselect('div.tabContainer div.narrativedetails')[0].text
#
#            print event_url, lxml.etree.tostring(event_price)

                

       
Main()

                        

