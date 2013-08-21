import scraperwiki
import urllib2
import datetime
import calendar
import tweepy
import bitlyapi
import cgi
import os
from BeautifulSoup import BeautifulSoup


# this brings in the API keys for twitter 
qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

BASE_URL = "http://www.inspections.vcha.ca"
BASE_SEARCH_STRING = "/Facility?report-type=ffffffff-ffff-ffff-ffff-fffffffffff1&area=839389f2-0c3c-11d6-9fb5-009027c3eece&sort-by=LastInspectedDate&alpha=&search-term=&submit-search=Search"

def scrapeSummaryPage(link, theDay, theMonth):
    page = urllib2.urlopen(BASE_URL + link)
    soup = BeautifulSoup(page)
    # just get first report at top - as we know last report is displayed first
    theInspectionLink = soup.findAll('a', {'href': lambda x : x.startswith('/Inspection/Show/')})[0]
    scrapeReport(theInspectionLink['href'], theDay, theMonth)

def scrapeReport(link, theDay, theMonth):
    page = urllib2.urlopen(BASE_URL + link)
    soup = BeautifulSoup(page)
    theSummaryTable = soup.findAll("table", { "class" : "columnar" })
    
    # get second table which contains whether or not re-inspection is needed
    rows = theSummaryTable[1].findChildren(['td'])

    # this determines whether a re-inspection is needed
    if str(rows[2].string).strip() == "True":
        theRestaurantName = soup.findAll("h3", { "class" : "bottom-border" })
        theAddress = soup.findAll("div", { "id" : "address" })

        # strip out 'Vancouver postal code' from address to shorten the tweet text
        theAddressStr=theAddress[0].text.strip()
        theAddressSubStr=theAddressStr[0:theAddressStr.find("Vancouver")]
        tweetReport(theRestaurantName[0].text + " (" + theAddressSubStr + ") was found with a safety deficiency on " + calendar.month_abbr[theMonth] + " " + str(theDay) + " " + getShortURL(BASE_URL + link) + " #vancouver")

def tweetReport(toTweet):
    auth = tweepy.OAuthHandler(qsenv["CONSUMER_KEY"], qsenv["CONSUMER_SECRET"])  
    auth.set_access_token(qsenv["ACCESS_KEY"], qsenv["ACCESS_SECRET"])
    api = tweepy.API(auth)
    try:
        api.update_status(toTweet)
    except:
        print "error: " + sys.exc_info()[1]
    print "tweeted: "+toTweet

def getShortURL(longURL):
    b = bitlyapi.BitLy(qsenv["BITLY_USER"], qsenv["BITLY_KEY"])
    newURL = b.shorten(longUrl=longURL)
    return newURL['url']





# assumption is we are running script day AFTER reports released i.e. run script on 26th to get reports for 25th

theDay = datetime.datetime.now().day - 1
theMonth = datetime.datetime.now().month

# if just started a new month don't want to return 0
if (datetime.datetime.now().month in [5, 7, 10, 12] and theDay == 0):
    theDay = 30
    theMonth = datetime.datetime.now().month - 1
elif (theDay == 0):
    theDay = 31
    theMonth = datetime.datetime.now().month - 1

page = urllib2.urlopen(BASE_URL + BASE_SEARCH_STRING)

soup = BeautifulSoup(page)

thedates = soup.findAll("td", { "class" : "center" })
theLinks = soup.findAll('a', {'href': lambda x : x.startswith('/Facility/Show/')}) 

counter = 0


for thedate in thedates:

    if theDay < 10:        
        if thedate.text[0:2] == str("0"+str(theDay)):
            scrapeSummaryPage(theLinks[counter]['href'], theDay, theMonth)     
            counter += 1        
        else:    
            #do nothing
            counter += 1
    else:
        if thedate.text[0:2] == str(theDay):
            scrapeSummaryPage(theLinks[counter]['href'], theDay, theMonth)     
            counter += 1        
        else:    
            #do nothing
            counter += 1
import scraperwiki
import urllib2
import datetime
import calendar
import tweepy
import bitlyapi
import cgi
import os
from BeautifulSoup import BeautifulSoup


# this brings in the API keys for twitter 
qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

BASE_URL = "http://www.inspections.vcha.ca"
BASE_SEARCH_STRING = "/Facility?report-type=ffffffff-ffff-ffff-ffff-fffffffffff1&area=839389f2-0c3c-11d6-9fb5-009027c3eece&sort-by=LastInspectedDate&alpha=&search-term=&submit-search=Search"

def scrapeSummaryPage(link, theDay, theMonth):
    page = urllib2.urlopen(BASE_URL + link)
    soup = BeautifulSoup(page)
    # just get first report at top - as we know last report is displayed first
    theInspectionLink = soup.findAll('a', {'href': lambda x : x.startswith('/Inspection/Show/')})[0]
    scrapeReport(theInspectionLink['href'], theDay, theMonth)

def scrapeReport(link, theDay, theMonth):
    page = urllib2.urlopen(BASE_URL + link)
    soup = BeautifulSoup(page)
    theSummaryTable = soup.findAll("table", { "class" : "columnar" })
    
    # get second table which contains whether or not re-inspection is needed
    rows = theSummaryTable[1].findChildren(['td'])

    # this determines whether a re-inspection is needed
    if str(rows[2].string).strip() == "True":
        theRestaurantName = soup.findAll("h3", { "class" : "bottom-border" })
        theAddress = soup.findAll("div", { "id" : "address" })

        # strip out 'Vancouver postal code' from address to shorten the tweet text
        theAddressStr=theAddress[0].text.strip()
        theAddressSubStr=theAddressStr[0:theAddressStr.find("Vancouver")]
        tweetReport(theRestaurantName[0].text + " (" + theAddressSubStr + ") was found with a safety deficiency on " + calendar.month_abbr[theMonth] + " " + str(theDay) + " " + getShortURL(BASE_URL + link) + " #vancouver")

def tweetReport(toTweet):
    auth = tweepy.OAuthHandler(qsenv["CONSUMER_KEY"], qsenv["CONSUMER_SECRET"])  
    auth.set_access_token(qsenv["ACCESS_KEY"], qsenv["ACCESS_SECRET"])
    api = tweepy.API(auth)
    try:
        api.update_status(toTweet)
    except:
        print "error: " + sys.exc_info()[1]
    print "tweeted: "+toTweet

def getShortURL(longURL):
    b = bitlyapi.BitLy(qsenv["BITLY_USER"], qsenv["BITLY_KEY"])
    newURL = b.shorten(longUrl=longURL)
    return newURL['url']





# assumption is we are running script day AFTER reports released i.e. run script on 26th to get reports for 25th

theDay = datetime.datetime.now().day - 1
theMonth = datetime.datetime.now().month

# if just started a new month don't want to return 0
if (datetime.datetime.now().month in [5, 7, 10, 12] and theDay == 0):
    theDay = 30
    theMonth = datetime.datetime.now().month - 1
elif (theDay == 0):
    theDay = 31
    theMonth = datetime.datetime.now().month - 1

page = urllib2.urlopen(BASE_URL + BASE_SEARCH_STRING)

soup = BeautifulSoup(page)

thedates = soup.findAll("td", { "class" : "center" })
theLinks = soup.findAll('a', {'href': lambda x : x.startswith('/Facility/Show/')}) 

counter = 0


for thedate in thedates:

    if theDay < 10:        
        if thedate.text[0:2] == str("0"+str(theDay)):
            scrapeSummaryPage(theLinks[counter]['href'], theDay, theMonth)     
            counter += 1        
        else:    
            #do nothing
            counter += 1
    else:
        if thedate.text[0:2] == str(theDay):
            scrapeSummaryPage(theLinks[counter]['href'], theDay, theMonth)     
            counter += 1        
        else:    
            #do nothing
            counter += 1
