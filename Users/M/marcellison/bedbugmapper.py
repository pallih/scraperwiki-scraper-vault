import scraperwiki
import urllib2
import datetime
import calendar
from BeautifulSoup import BeautifulSoup
from geopy import geocoders  


def mapAddress(theAddress):

    g = geocoders.Google()
    place, (lat, lng) = g.geocode(theAddress)  
    print (place, lat, lng) 


    scraperwiki.sqlite.execute("insert into locations values (?,?,?,?)", (theAddress, datetime.date.today().strftime('%m/%d/%Y'), str(lng), str(lat)))
    # scraperwiki.sqlite.execute("insert into locations values (?,?,?,?)", (theAddress, '05/16/2012', str(lng), str(lat)))
    scraperwiki.sqlite.commit() 


    result = scraperwiki.sqlite.execute("select * from locations")
    print result




BASE_SEARCH_STRING = "http://bedbugregistry.com"
RECENT_SEARCH_STRING = "/metro/vancouver/recent"

page = urllib2.urlopen(BASE_SEARCH_STRING + RECENT_SEARCH_STRING)

soup = BeautifulSoup(page)


#thedates = soup.findAll("p", { "style" : "font-weight:bold" })
theLinks = soup.findAll('a', {'href': lambda x : x.startswith('/location/BC/')}) 

counter = 0


for theLink in theLinks:
    newurl=theLink['href'].replace(' ','%20')
    print newurl
    page = urllib2.urlopen(BASE_SEARCH_STRING + newurl)
    soup = BeautifulSoup(page)
    thedates = soup.findAll("span", { "class" : "submit_date" })
    theaddresses = soup.findAll("span", { "class" : "address" })
    # only get first should be todays - if not break loop and finish routine - means reached end of any of todays reports.
    print "the dates" + thedates[0].text
    if (thedates[0].text == datetime.date.today().strftime('%m/%d/%Y')):
    # if (thedates[0].text == datetime.date.today().strftime('05/16/2012')):
        print "match: tweet/map"
        mapAddress(theaddresses[0].text + ", Vancouver, BC, Canada")
    else:
        print "no match on todays date"
        # break


#scraperwiki.sqlite.execute("create table locations (`address` string, `the_date` text, `longitude` text, `latitude` text)")


import scraperwiki
import urllib2
import datetime
import calendar
from BeautifulSoup import BeautifulSoup
from geopy import geocoders  


def mapAddress(theAddress):

    g = geocoders.Google()
    place, (lat, lng) = g.geocode(theAddress)  
    print (place, lat, lng) 


    scraperwiki.sqlite.execute("insert into locations values (?,?,?,?)", (theAddress, datetime.date.today().strftime('%m/%d/%Y'), str(lng), str(lat)))
    # scraperwiki.sqlite.execute("insert into locations values (?,?,?,?)", (theAddress, '05/16/2012', str(lng), str(lat)))
    scraperwiki.sqlite.commit() 


    result = scraperwiki.sqlite.execute("select * from locations")
    print result




BASE_SEARCH_STRING = "http://bedbugregistry.com"
RECENT_SEARCH_STRING = "/metro/vancouver/recent"

page = urllib2.urlopen(BASE_SEARCH_STRING + RECENT_SEARCH_STRING)

soup = BeautifulSoup(page)


#thedates = soup.findAll("p", { "style" : "font-weight:bold" })
theLinks = soup.findAll('a', {'href': lambda x : x.startswith('/location/BC/')}) 

counter = 0


for theLink in theLinks:
    newurl=theLink['href'].replace(' ','%20')
    print newurl
    page = urllib2.urlopen(BASE_SEARCH_STRING + newurl)
    soup = BeautifulSoup(page)
    thedates = soup.findAll("span", { "class" : "submit_date" })
    theaddresses = soup.findAll("span", { "class" : "address" })
    # only get first should be todays - if not break loop and finish routine - means reached end of any of todays reports.
    print "the dates" + thedates[0].text
    if (thedates[0].text == datetime.date.today().strftime('%m/%d/%Y')):
    # if (thedates[0].text == datetime.date.today().strftime('05/16/2012')):
        print "match: tweet/map"
        mapAddress(theaddresses[0].text + ", Vancouver, BC, Canada")
    else:
        print "no match on todays date"
        # break


#scraperwiki.sqlite.execute("create table locations (`address` string, `the_date` text, `longitude` text, `latitude` text)")


import scraperwiki
import urllib2
import datetime
import calendar
from BeautifulSoup import BeautifulSoup
from geopy import geocoders  


def mapAddress(theAddress):

    g = geocoders.Google()
    place, (lat, lng) = g.geocode(theAddress)  
    print (place, lat, lng) 


    scraperwiki.sqlite.execute("insert into locations values (?,?,?,?)", (theAddress, datetime.date.today().strftime('%m/%d/%Y'), str(lng), str(lat)))
    # scraperwiki.sqlite.execute("insert into locations values (?,?,?,?)", (theAddress, '05/16/2012', str(lng), str(lat)))
    scraperwiki.sqlite.commit() 


    result = scraperwiki.sqlite.execute("select * from locations")
    print result




BASE_SEARCH_STRING = "http://bedbugregistry.com"
RECENT_SEARCH_STRING = "/metro/vancouver/recent"

page = urllib2.urlopen(BASE_SEARCH_STRING + RECENT_SEARCH_STRING)

soup = BeautifulSoup(page)


#thedates = soup.findAll("p", { "style" : "font-weight:bold" })
theLinks = soup.findAll('a', {'href': lambda x : x.startswith('/location/BC/')}) 

counter = 0


for theLink in theLinks:
    newurl=theLink['href'].replace(' ','%20')
    print newurl
    page = urllib2.urlopen(BASE_SEARCH_STRING + newurl)
    soup = BeautifulSoup(page)
    thedates = soup.findAll("span", { "class" : "submit_date" })
    theaddresses = soup.findAll("span", { "class" : "address" })
    # only get first should be todays - if not break loop and finish routine - means reached end of any of todays reports.
    print "the dates" + thedates[0].text
    if (thedates[0].text == datetime.date.today().strftime('%m/%d/%Y')):
    # if (thedates[0].text == datetime.date.today().strftime('05/16/2012')):
        print "match: tweet/map"
        mapAddress(theaddresses[0].text + ", Vancouver, BC, Canada")
    else:
        print "no match on todays date"
        # break


#scraperwiki.sqlite.execute("create table locations (`address` string, `the_date` text, `longitude` text, `latitude` text)")


import scraperwiki
import urllib2
import datetime
import calendar
from BeautifulSoup import BeautifulSoup
from geopy import geocoders  


def mapAddress(theAddress):

    g = geocoders.Google()
    place, (lat, lng) = g.geocode(theAddress)  
    print (place, lat, lng) 


    scraperwiki.sqlite.execute("insert into locations values (?,?,?,?)", (theAddress, datetime.date.today().strftime('%m/%d/%Y'), str(lng), str(lat)))
    # scraperwiki.sqlite.execute("insert into locations values (?,?,?,?)", (theAddress, '05/16/2012', str(lng), str(lat)))
    scraperwiki.sqlite.commit() 


    result = scraperwiki.sqlite.execute("select * from locations")
    print result




BASE_SEARCH_STRING = "http://bedbugregistry.com"
RECENT_SEARCH_STRING = "/metro/vancouver/recent"

page = urllib2.urlopen(BASE_SEARCH_STRING + RECENT_SEARCH_STRING)

soup = BeautifulSoup(page)


#thedates = soup.findAll("p", { "style" : "font-weight:bold" })
theLinks = soup.findAll('a', {'href': lambda x : x.startswith('/location/BC/')}) 

counter = 0


for theLink in theLinks:
    newurl=theLink['href'].replace(' ','%20')
    print newurl
    page = urllib2.urlopen(BASE_SEARCH_STRING + newurl)
    soup = BeautifulSoup(page)
    thedates = soup.findAll("span", { "class" : "submit_date" })
    theaddresses = soup.findAll("span", { "class" : "address" })
    # only get first should be todays - if not break loop and finish routine - means reached end of any of todays reports.
    print "the dates" + thedates[0].text
    if (thedates[0].text == datetime.date.today().strftime('%m/%d/%Y')):
    # if (thedates[0].text == datetime.date.today().strftime('05/16/2012')):
        print "match: tweet/map"
        mapAddress(theaddresses[0].text + ", Vancouver, BC, Canada")
    else:
        print "no match on todays date"
        # break


#scraperwiki.sqlite.execute("create table locations (`address` string, `the_date` text, `longitude` text, `latitude` text)")


