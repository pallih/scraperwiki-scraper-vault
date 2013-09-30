__version__ = '0.1'
__author__ = 'antmancoder'

import scraperwiki
import lxml.html
import urlparse
import urllib2
import re
import dateutil.parser
from geopy import geocoders

# Introduction of various global variables required throughout the running of the code
URLSTEM = "http://planecrashinfo.com"
URLYEARDB = "database.htm"
YEARSOURCE = urlparse.urljoin(URLSTEM, URLYEARDB)
YEARLIST = []
SOURCEPAGEURL = []


def parenturlscraper():
    """Function scrapes all of the parent URLs from 'planecrashinfo.com/database'"""
    html = scraperwiki.scrape(YEARSOURCE)
    root = lxml.html.fromstring(html)

    hrefs = root.cssselect('td a')

    for href in hrefs:
        link = href.attrib['href']
        url = urlparse.urljoin(URLSTEM, link)
        YEARLIST.append(url)

def childurlscraper():
    """Function scrapes all of the child URLs from those scraped in the parenturlscraper module"""
    for url in YEARLIST:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        hrefs = root.cssselect('td a')
        url = url[0:34]
        for href in hrefs:
            linkurl = href.attrib['href']
            url = urlparse.urljoin(url, linkurl)
            SOURCEPAGEURL.append(url)

def sourcepagescraper(): 
    """Function scrapes respective data for each accident and placed it into DB"""
    for url in SOURCEPAGEURL:
        try: 
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            for tr in root.cssselect("body"):
                tds = tr.cssselect("td")
                location = coorlookup(tds[7].text_content())
                #aboard = statsextraction(tds[21].text_content())
                #fatalities = statsextraction(tds[23].text_content())
                for td in tds:
                    crashinfo = {}
                    crashinfo['URL'] = url
                    crashinfo['Date'] = dateutil.parser.parse(tds[3].text_content()).date()
                    crashinfo['Time'] = tds[5].text_content()
                    crashinfo['Location'] = tds[7].text_content()
                    crashinfo['Latitude'] = location[1][0]
                    crashinfo['Longitude'] = location[1][1]
                    crashinfo['Operator'] = tds[9].text_content()
                    crashinfo['Flight Number'] = tds[11].text_content()
                    crashinfo['Route'] = tds[13].text_content()
                    crashinfo['Aircraft Type'] = tds[15].text_content()
                    crashinfo['Registration'] = tds[17].text_content()
                    crashinfo['Fuselage Number'] = tds[19].text_content()
                    crashinfo['Aboard'] = tds[21].text_content()
                    crashinfo['Fatalities'] = tds[23].text_content()                   
                    #crashinfo['Passengers Aboard'] = aboard[0]
                    #crashinfo['Crew Aboard'] = aboard[1]
                    #crashinfo['Passenger Fatalities'] = fatalities[0]
                    #crashinfo['Crew Fatalities'] = fatalities[1]
                    crashinfo['Ground Fatalities'] = tds[25].text_content()
                    crashinfo['Summary'] = tds[27].text_content()

                scraperwiki.sqlite.save(unique_keys=['URL'], data=crashinfo)
        except urllib2.HTTPError, err:
            if err.code == 404:
                continue

#def statsextraction(people):
 #   """Function to strip out the number of passengers and crew from string"""
  #  print people, "has a type", type(people)
   # numbers = re.compile(r'\(\s*passengers:\s*(\d{1,3}|\?)\s+ crew:\s*(\d{1,3}|\?)\s*\)')
    #print numbers.search(people).groups()
     #return numbers.search(people).groups()

def coorlookup(location):
    """Function is called from the 'sourcepagescraper' function to geolocate locations listed on website for each accident"""
    geolocate = geocoders.Google()
    try:
        loc = geolocate.geocode(location, exactly_one=True)
        return loc
    except:
        return ("",("",""))

parenturlscraper()
childurlscraper()
sourcepagescraper()


    
    
__version__ = '0.1'
__author__ = 'antmancoder'

import scraperwiki
import lxml.html
import urlparse
import urllib2
import re
import dateutil.parser
from geopy import geocoders

# Introduction of various global variables required throughout the running of the code
URLSTEM = "http://planecrashinfo.com"
URLYEARDB = "database.htm"
YEARSOURCE = urlparse.urljoin(URLSTEM, URLYEARDB)
YEARLIST = []
SOURCEPAGEURL = []


def parenturlscraper():
    """Function scrapes all of the parent URLs from 'planecrashinfo.com/database'"""
    html = scraperwiki.scrape(YEARSOURCE)
    root = lxml.html.fromstring(html)

    hrefs = root.cssselect('td a')

    for href in hrefs:
        link = href.attrib['href']
        url = urlparse.urljoin(URLSTEM, link)
        YEARLIST.append(url)

def childurlscraper():
    """Function scrapes all of the child URLs from those scraped in the parenturlscraper module"""
    for url in YEARLIST:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        hrefs = root.cssselect('td a')
        url = url[0:34]
        for href in hrefs:
            linkurl = href.attrib['href']
            url = urlparse.urljoin(url, linkurl)
            SOURCEPAGEURL.append(url)

def sourcepagescraper(): 
    """Function scrapes respective data for each accident and placed it into DB"""
    for url in SOURCEPAGEURL:
        try: 
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            for tr in root.cssselect("body"):
                tds = tr.cssselect("td")
                location = coorlookup(tds[7].text_content())
                #aboard = statsextraction(tds[21].text_content())
                #fatalities = statsextraction(tds[23].text_content())
                for td in tds:
                    crashinfo = {}
                    crashinfo['URL'] = url
                    crashinfo['Date'] = dateutil.parser.parse(tds[3].text_content()).date()
                    crashinfo['Time'] = tds[5].text_content()
                    crashinfo['Location'] = tds[7].text_content()
                    crashinfo['Latitude'] = location[1][0]
                    crashinfo['Longitude'] = location[1][1]
                    crashinfo['Operator'] = tds[9].text_content()
                    crashinfo['Flight Number'] = tds[11].text_content()
                    crashinfo['Route'] = tds[13].text_content()
                    crashinfo['Aircraft Type'] = tds[15].text_content()
                    crashinfo['Registration'] = tds[17].text_content()
                    crashinfo['Fuselage Number'] = tds[19].text_content()
                    crashinfo['Aboard'] = tds[21].text_content()
                    crashinfo['Fatalities'] = tds[23].text_content()                   
                    #crashinfo['Passengers Aboard'] = aboard[0]
                    #crashinfo['Crew Aboard'] = aboard[1]
                    #crashinfo['Passenger Fatalities'] = fatalities[0]
                    #crashinfo['Crew Fatalities'] = fatalities[1]
                    crashinfo['Ground Fatalities'] = tds[25].text_content()
                    crashinfo['Summary'] = tds[27].text_content()

                scraperwiki.sqlite.save(unique_keys=['URL'], data=crashinfo)
        except urllib2.HTTPError, err:
            if err.code == 404:
                continue

#def statsextraction(people):
 #   """Function to strip out the number of passengers and crew from string"""
  #  print people, "has a type", type(people)
   # numbers = re.compile(r'\(\s*passengers:\s*(\d{1,3}|\?)\s+ crew:\s*(\d{1,3}|\?)\s*\)')
    #print numbers.search(people).groups()
     #return numbers.search(people).groups()

def coorlookup(location):
    """Function is called from the 'sourcepagescraper' function to geolocate locations listed on website for each accident"""
    geolocate = geocoders.Google()
    try:
        loc = geolocate.geocode(location, exactly_one=True)
        return loc
    except:
        return ("",("",""))

parenturlscraper()
childurlscraper()
sourcepagescraper()


    
    
