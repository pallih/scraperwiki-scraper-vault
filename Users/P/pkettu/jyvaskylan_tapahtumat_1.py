# -*- coding: utf-8 -*-
###############################################################################
# Basic scraper
###############################################################################
# http://bigclean.org/ event in Jyväskylä 19.3.2010
#
# edited 8.5.2012 to support event types

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime

# http://www3.jkl.fi/tapahtumat/main.php?date=20110319&kunta=1&rajaa=0 
# max 20 kerralla
# >>Näytä seuraavat 20

# scrape_events function: gets passed an individual page to scrape
def scrape_events( events, event_type ):
    for event in events:
        #print event.prettify()

        record = {}
        title = event.a

        #print title.renderContents()
        lis = event.findAll( "li" )
        #print lis[0].renderContents()
        #print lis[1].renderContents()
        #print lis[2].renderContents()
        #print lis[3].renderContents()

        record[ 'title' ] = title.renderContents()

        record[ 'event_type_id' ] = event_type;

        for lis_item in lis:

            string_item = str ( lis_item.renderContents() )    
            
            if string_item.startswith("Paikka:"):
                record[ 'place' ] = lis_item.renderContents() 
            elif string_item.startswith("Osoite:"):
                record[ 'address' ] = lis_item.renderContents()
            elif string_item.startswith("Klo:"):
                record[ 'time' ] = lis_item.renderContents()
            else:
                record[ 'date' ] = lis_item.renderContents()

        print record, '------------'

        try:
            scraperwiki.datastore.save( [ 'date', 'title' ], record )
        except UnicodeDecodeError:
            print "UnicodeDecodeError in event: " + title.renderContents()
        

# scrape_and_look_for_next_link function: calls the scrape_events
# function, then hunts for a 'next' link: if one is found, calls itself again
# starting_url = 'http://www3.jkl.fi/tapahtumat/main.php?date=20110319&kunta=1&rajaa=0'
def scrape_and_look_for_next_link( url, date, event_type, index ):

    url = url + "?date=" + date + "&kunta=1" + "&hLuokka[]=" + str( event_type ) + "&rajaa=" + str( index )
    print "fetching url: " + url
    html = scraperwiki.scrape( url )
    soup = BeautifulSoup( html )
    events = soup.findAll( "div", "tapahtumatiedot" )
    scrape_events( events , event_type )

    # if 3 are found then there are more pages
    links = soup.findAll( "span", "pieni" )
    if len( links ) == 3:
        index = index + 20
        scrape_and_look_for_next_link( base_url, date, index )

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www3.jkl.fi/tapahtumat/main.php'
date = datetime.datetime.now().strftime("%Y%m%d")
event_types = [16,32,33,35,30,17,23,18,19,10,11,8,6,12,1,2,4,7,14,20,15,28,21,29]



# retrieve a page

for event_type in event_types:
    scrape_and_look_for_next_link( base_url,date,event_type, 0 )
    

# -*- coding: utf-8 -*-
###############################################################################
# Basic scraper
###############################################################################
# http://bigclean.org/ event in Jyväskylä 19.3.2010
#
# edited 8.5.2012 to support event types

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime

# http://www3.jkl.fi/tapahtumat/main.php?date=20110319&kunta=1&rajaa=0 
# max 20 kerralla
# >>Näytä seuraavat 20

# scrape_events function: gets passed an individual page to scrape
def scrape_events( events, event_type ):
    for event in events:
        #print event.prettify()

        record = {}
        title = event.a

        #print title.renderContents()
        lis = event.findAll( "li" )
        #print lis[0].renderContents()
        #print lis[1].renderContents()
        #print lis[2].renderContents()
        #print lis[3].renderContents()

        record[ 'title' ] = title.renderContents()

        record[ 'event_type_id' ] = event_type;

        for lis_item in lis:

            string_item = str ( lis_item.renderContents() )    
            
            if string_item.startswith("Paikka:"):
                record[ 'place' ] = lis_item.renderContents() 
            elif string_item.startswith("Osoite:"):
                record[ 'address' ] = lis_item.renderContents()
            elif string_item.startswith("Klo:"):
                record[ 'time' ] = lis_item.renderContents()
            else:
                record[ 'date' ] = lis_item.renderContents()

        print record, '------------'

        try:
            scraperwiki.datastore.save( [ 'date', 'title' ], record )
        except UnicodeDecodeError:
            print "UnicodeDecodeError in event: " + title.renderContents()
        

# scrape_and_look_for_next_link function: calls the scrape_events
# function, then hunts for a 'next' link: if one is found, calls itself again
# starting_url = 'http://www3.jkl.fi/tapahtumat/main.php?date=20110319&kunta=1&rajaa=0'
def scrape_and_look_for_next_link( url, date, event_type, index ):

    url = url + "?date=" + date + "&kunta=1" + "&hLuokka[]=" + str( event_type ) + "&rajaa=" + str( index )
    print "fetching url: " + url
    html = scraperwiki.scrape( url )
    soup = BeautifulSoup( html )
    events = soup.findAll( "div", "tapahtumatiedot" )
    scrape_events( events , event_type )

    # if 3 are found then there are more pages
    links = soup.findAll( "span", "pieni" )
    if len( links ) == 3:
        index = index + 20
        scrape_and_look_for_next_link( base_url, date, index )

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www3.jkl.fi/tapahtumat/main.php'
date = datetime.datetime.now().strftime("%Y%m%d")
event_types = [16,32,33,35,30,17,23,18,19,10,11,8,6,12,1,2,4,7,14,20,15,28,21,29]



# retrieve a page

for event_type in event_types:
    scrape_and_look_for_next_link( base_url,date,event_type, 0 )
    

