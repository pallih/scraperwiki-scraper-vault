# -*- coding: utf-8 -*-
###############################################################################
# Basic scraper
###############################################################################
# http://bigclean.org/ event in Jyväskylä 19.3.2010
#

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime

# http://klubitus.org/kalenteri.php

# scrape_events function: gets passed an individual page to scrape
def scrape_events( events ):
    for event in events:

        print event.prettify()
        #print 'CLASS: '+event['class']

        if event['class'] == 'header':
            eventDate = event.th.renderContents()
            eventDate = eventDate[eventDate.find(' ')+1:len(eventDate)]
            print 'DATE: '+eventDate

        if event['class'] == 'even' or event['class'] == 'odd':
            #print 'JEE'
            #fly = event.td[0]
            eventCells = event.findAll('td')
            #print eventCells
            
            # jos rivillä 3 solua, kyseessä on eventti, muuten googlemainos
            if len(eventCells) == 3:
                eventCell = eventCells[1]
                #print 'EVENTTI'
                #print eventCell
                #eventCell = event.td
                title = eventCell.a.renderContents()
                info = eventCell.findAll('span', {'class' : 'eventinfo'})[0].renderContents()
                place = eventCell.findAll('span', {'class' : 'place'})[0].renderContents()
                city = eventCells[2].renderContents()
                desc = "TODO: must be scraped from event's own page"
                #print 'title: '+title+', info: '+info+', place: '+place+', city: '+city+', date: '+eventDate;

                record = {}
                record['title'] = title
                record['info'] = info
                record['description'] = desc
                record['place'] = place
                record['city'] = city
                record['date'] = eventDate

                print 'event: ', record

                try:
                    scraperwiki.datastore.save( [ 'date', 'title' ], record )
                except UnicodeDecodeError:
                    print "UnicodeDecodeError in event: " + title.renderContents()


        #record = {}
        #title = event.a

        #print title.renderContents()
        #lis = event.findAll( "li" )
        #print lis[0].renderContents()
        #print lis[1].renderContents()
        #print lis[2].renderContents()
        #print lis[3].renderContents()

        #record[ 'title' ] = title.renderContents()
        #record[ 'date' ] = lis[0].renderContents()
        #record[ 'time' ] = lis[1].renderContents() 
        #if len(lis) > 2: 
        #    record[ 'place' ] = lis[2].renderContents() 
        #else:
        #    record[ 'place' ] = "Jkl"
        #if len(lis) > 3:
        #    record[ 'address' ] = lis[3].renderContents() 
        #else:
        #    record[ 'address' ] = "Jkl"

        #print record, '------------'

        #try:
        #    scraperwiki.datastore.save( [ 'date', 'title' ], record )
        #except UnicodeDecodeError:
        #    print "UnicodeDecodeError in event: " + title.renderContents()

        print '------------'
        

# scrape_and_look_for_next_link function: calls the scrape_events
# function, then hunts for a 'next' link: if one is found, calls itself again
# starting_url = 'http://www3.jkl.fi/tapahtumat/main.php?date=20110319&kunta=1&rajaa=0'
def scrape_and_look_for_next_link( url, date, index ):

    #url = url + "?date=" + date + "&kunta=1" + "&rajaa=" + str( index )
    print "fetching url: " + url
    html = scraperwiki.scrape( url )
    soup = BeautifulSoup( html )
    events = soup.findAll( "tr" )
    scrape_events( events )

    # if 3 are found then there are more pages
    #links = soup.findAll( "span", "pieni" )
    #if len( links ) == 3:
    #    index = index + 20
    #    scrape_and_look_for_next_link( base_url, date, index )

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://klubitus.org/kalenteri.php'
date = datetime.datetime.now().strftime("%Y%m%d")
eventDate = 'UNDEFINED'

# retrieve a page
scrape_and_look_for_next_link( base_url, date, 0 )
    

# -*- coding: utf-8 -*-
###############################################################################
# Basic scraper
###############################################################################
# http://bigclean.org/ event in Jyväskylä 19.3.2010
#

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime

# http://klubitus.org/kalenteri.php

# scrape_events function: gets passed an individual page to scrape
def scrape_events( events ):
    for event in events:

        print event.prettify()
        #print 'CLASS: '+event['class']

        if event['class'] == 'header':
            eventDate = event.th.renderContents()
            eventDate = eventDate[eventDate.find(' ')+1:len(eventDate)]
            print 'DATE: '+eventDate

        if event['class'] == 'even' or event['class'] == 'odd':
            #print 'JEE'
            #fly = event.td[0]
            eventCells = event.findAll('td')
            #print eventCells
            
            # jos rivillä 3 solua, kyseessä on eventti, muuten googlemainos
            if len(eventCells) == 3:
                eventCell = eventCells[1]
                #print 'EVENTTI'
                #print eventCell
                #eventCell = event.td
                title = eventCell.a.renderContents()
                info = eventCell.findAll('span', {'class' : 'eventinfo'})[0].renderContents()
                place = eventCell.findAll('span', {'class' : 'place'})[0].renderContents()
                city = eventCells[2].renderContents()
                desc = "TODO: must be scraped from event's own page"
                #print 'title: '+title+', info: '+info+', place: '+place+', city: '+city+', date: '+eventDate;

                record = {}
                record['title'] = title
                record['info'] = info
                record['description'] = desc
                record['place'] = place
                record['city'] = city
                record['date'] = eventDate

                print 'event: ', record

                try:
                    scraperwiki.datastore.save( [ 'date', 'title' ], record )
                except UnicodeDecodeError:
                    print "UnicodeDecodeError in event: " + title.renderContents()


        #record = {}
        #title = event.a

        #print title.renderContents()
        #lis = event.findAll( "li" )
        #print lis[0].renderContents()
        #print lis[1].renderContents()
        #print lis[2].renderContents()
        #print lis[3].renderContents()

        #record[ 'title' ] = title.renderContents()
        #record[ 'date' ] = lis[0].renderContents()
        #record[ 'time' ] = lis[1].renderContents() 
        #if len(lis) > 2: 
        #    record[ 'place' ] = lis[2].renderContents() 
        #else:
        #    record[ 'place' ] = "Jkl"
        #if len(lis) > 3:
        #    record[ 'address' ] = lis[3].renderContents() 
        #else:
        #    record[ 'address' ] = "Jkl"

        #print record, '------------'

        #try:
        #    scraperwiki.datastore.save( [ 'date', 'title' ], record )
        #except UnicodeDecodeError:
        #    print "UnicodeDecodeError in event: " + title.renderContents()

        print '------------'
        

# scrape_and_look_for_next_link function: calls the scrape_events
# function, then hunts for a 'next' link: if one is found, calls itself again
# starting_url = 'http://www3.jkl.fi/tapahtumat/main.php?date=20110319&kunta=1&rajaa=0'
def scrape_and_look_for_next_link( url, date, index ):

    #url = url + "?date=" + date + "&kunta=1" + "&rajaa=" + str( index )
    print "fetching url: " + url
    html = scraperwiki.scrape( url )
    soup = BeautifulSoup( html )
    events = soup.findAll( "tr" )
    scrape_events( events )

    # if 3 are found then there are more pages
    #links = soup.findAll( "span", "pieni" )
    #if len( links ) == 3:
    #    index = index + 20
    #    scrape_and_look_for_next_link( base_url, date, index )

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://klubitus.org/kalenteri.php'
date = datetime.datetime.now().strftime("%Y%m%d")
eventDate = 'UNDEFINED'

# retrieve a page
scrape_and_look_for_next_link( base_url, date, 0 )
    

