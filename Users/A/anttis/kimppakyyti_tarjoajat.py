# -*- coding: utf-8 -*-
###############################################################################
# Basic scraper
###############################################################################
# 
#

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime

# http://kimppa.net/Hae_Tarjoaja.aspx
# pvm: /html/body/form/div[3]/div[3]/table/tbody/tr[2]/td[2]

# scrape_events function: gets passed an individual page to scrape
def scrape_events( events ):
    for event in events:

#        print event.prettify()

        record = {}
#        title = event.a

        #print title.renderContents()
        lis = event.findAll( "td" )
        #print lis[0].renderContents()
        #print lis[1].renderContents()
        #print lis[2].renderContents()
        #print lis[3].renderContents()

#        record[ 'title' ] = title.renderContents()
        record[ 'date' ] = lis[1].font.renderContents()
        record[ 'from' ] = lis[2].font.renderContents() 
        record[ 'timeOfDeparture' ] = lis[3].font.renderContents() 
        record[ 'via' ] = lis[4].font.renderContents() 
        record[ 'to' ] = lis[5].font.renderContents() 
        record[ 'vehicle' ] = lis[6].font.renderContents() 
        record[ 'timeOfArrival' ] = lis[7].font.renderContents() 
        record[ 'info' ] = lis[8].font.renderContents() 
        record[ 'name' ] = lis[9].font.renderContents() 
        record[ 'phone' ] = lis[10].font.renderContents() 
        record[ 'mail' ] = lis[11].font.renderContents() 

        #print record, '------------'

        try:
            scraperwiki.datastore.save( [ 'date', 'from' ], record )
        except UnicodeDecodeError:
            print "UnicodeDecodeError in event: " + title.renderContents()
        

# scrape_and_look_for_next_link function: calls the scrape_events
# function, then hunts for a 'next' link: if one is found, calls itself again
# starting_url = 'http://www3.jkl.fi/tapahtumat/main.php?date=20110319&kunta=1&rajaa=0'
def scrape_and_look_for_next_link( url, date, index ):

    #url = url + "?date=" + date + "&kunta=1" + "&rajaa=" + str( index )
    print "fetching url: " + url
    html = scraperwiki.scrape( url )
    soup = BeautifulSoup( html )
    #events = soup.findAll( "div", "tapahtumatiedot" )
    #events = soup.findAll( style="background-color: WhiteSmoke; border-color: DarkSlateGray; border-style: inset; font-weight: normal;" )
    events = soup.findAll( "tr", bgcolor="WhiteSmoke" )
    print events
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
base_url = 'http://kimppa.net/Hae_Tarjoaja.aspx'
date = datetime.datetime.now().strftime("%Y%m%d")

# retrieve a page
scrape_and_look_for_next_link( base_url, date, 0 )
    
# -*- coding: utf-8 -*-
###############################################################################
# Basic scraper
###############################################################################
# 
#

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime

# http://kimppa.net/Hae_Tarjoaja.aspx
# pvm: /html/body/form/div[3]/div[3]/table/tbody/tr[2]/td[2]

# scrape_events function: gets passed an individual page to scrape
def scrape_events( events ):
    for event in events:

#        print event.prettify()

        record = {}
#        title = event.a

        #print title.renderContents()
        lis = event.findAll( "td" )
        #print lis[0].renderContents()
        #print lis[1].renderContents()
        #print lis[2].renderContents()
        #print lis[3].renderContents()

#        record[ 'title' ] = title.renderContents()
        record[ 'date' ] = lis[1].font.renderContents()
        record[ 'from' ] = lis[2].font.renderContents() 
        record[ 'timeOfDeparture' ] = lis[3].font.renderContents() 
        record[ 'via' ] = lis[4].font.renderContents() 
        record[ 'to' ] = lis[5].font.renderContents() 
        record[ 'vehicle' ] = lis[6].font.renderContents() 
        record[ 'timeOfArrival' ] = lis[7].font.renderContents() 
        record[ 'info' ] = lis[8].font.renderContents() 
        record[ 'name' ] = lis[9].font.renderContents() 
        record[ 'phone' ] = lis[10].font.renderContents() 
        record[ 'mail' ] = lis[11].font.renderContents() 

        #print record, '------------'

        try:
            scraperwiki.datastore.save( [ 'date', 'from' ], record )
        except UnicodeDecodeError:
            print "UnicodeDecodeError in event: " + title.renderContents()
        

# scrape_and_look_for_next_link function: calls the scrape_events
# function, then hunts for a 'next' link: if one is found, calls itself again
# starting_url = 'http://www3.jkl.fi/tapahtumat/main.php?date=20110319&kunta=1&rajaa=0'
def scrape_and_look_for_next_link( url, date, index ):

    #url = url + "?date=" + date + "&kunta=1" + "&rajaa=" + str( index )
    print "fetching url: " + url
    html = scraperwiki.scrape( url )
    soup = BeautifulSoup( html )
    #events = soup.findAll( "div", "tapahtumatiedot" )
    #events = soup.findAll( style="background-color: WhiteSmoke; border-color: DarkSlateGray; border-style: inset; font-weight: normal;" )
    events = soup.findAll( "tr", bgcolor="WhiteSmoke" )
    print events
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
base_url = 'http://kimppa.net/Hae_Tarjoaja.aspx'
date = datetime.datetime.now().strftime("%Y%m%d")

# retrieve a page
scrape_and_look_for_next_link( base_url, date, 0 )
    
