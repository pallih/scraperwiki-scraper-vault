import scraperwiki
import lxml.html
import re
import datetime


#Define HTML Stripper
from HTMLParser import HTMLParser
    
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
    
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()





# Get Page
html = scraperwiki.scrape("http://www.asthma.org.au/PollenAlert.aspx")
#Requires lxml.html           
root = lxml.html.fromstring(html)# turn our HTML into an lxml object

#N for Loop
n=0

#Increase range for more values - 163 total on page as of 8/11/2011)
for r in range(216):
    print "########## Round ",n," ##########"
    #Get Latest Pollen Rating
    LatestRating = root.cssselect("div.ModDNNUserDefinedTableC h2")[n]           
    print "Rating: ", LatestRating.text
    
    #Get Date of Latest Pollen Rating    
    LatestRatingDate = root.cssselect("div.ModDNNUserDefinedTableC td")[n*18+5]
    DateDirty=lxml.html.tostring(LatestRatingDate)
    #print "DateDirty= ", DateDirty
    LatestRatingDate =strip_tags(DateDirty)
    #print "LatestRatingDateStripped = ", LatestRatingDate
    #Convert Dates
    #import datetime
    LatestRatingDate = datetime.datetime.strptime(LatestRatingDate, '%d/%m/%Y').date()
    print "LatestRatingDateProcessed = ", LatestRatingDate

    
    #Count Grass & Total Pollen
    #import re
    gcm = root.cssselect("div.ModDNNUserDefinedTableC td")[n*18+8]
    gcm = gcm.text
    print "GCM: ",gcm
    match = re.search('([\d]+)[.|/]([\d]+)', gcm)
    GrassCount = match.group(1)
    TotalCount = match.group(2)
    
    
    #Save Ratings
    scraperwiki.sqlite.save(unique_keys=["Date"], data={"Date":LatestRatingDate, "Rating":LatestRating.text, "GrassCount":GrassCount, "TotalCount":TotalCount})
    
    n=n+1
    #reset values
    gcm = 0
    LatestRatingDate = 0
    GrassCount = 0
    TotalCount = 0
    match = 0
    LatestRatingDate = 0
    LatestRating = 0
    DateDirty = 0
    


# ###Twitter Posting
# import os, cgi
# qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
# 
# #Define Tweet
# record = scraperwiki.sqlite.select("* from `swdata` order by Date desc limit 1")[0]
# #print "Record= ", record
# #print "Rating = ", record['Rating']
# Date=record['Date']
# 
# #MessageText = "Today is rated ", record['Rating'], " for pollen. There are ", record['GrassCount'], "grains of grass pollen and ", record['TotalCount'], " total pollen grains. (Date: ", record['Date'], ")"
# 
# msg = 'Today is rated {Rating} for pollen. There are {GrassCount} grains of grass pollen and {TotalCount} total pollen grains per cubic metre.'.format(Rating=record['Rating'], GrassCount=record['GrassCount'], TotalCount=record['TotalCount'])
# #Also used to tweet (Date: {Date}) with Date=record['Date']
# 
# #Tweeting Function
# import tweepy
# def sendtweet(msg):
#     try:
#         #import locale
#         #import time
#         locale.setlocale(locale.LC_TIME, 'C')
#         auth = tweepy.OAuthHandler(qsenv["CONSUMER_KEY"], qsenv["CONSUMER_SECRET"])  
#         auth.set_access_token(qsenv["ACCESS_KEY"], qsenv["ACCESS_SECRET"])
#         api = tweepy.API(auth)
#         api.update_status(msg)
#         locale.setlocale(locale.LC_TIME, '')
#     except Exception, e:
#         print 'Failed to send tweet: %s' % msg
#         print e
# 
# 
# #Check if data is fresh (i.e. date on data matches today's date) - if not, send tweet to let people know that it's not coming.
# import time
# import locale
# import os
# from datetime import date
# os.environ['TZ'] = 'Australia/Melbourne'
# time.tzset()
# 
# if time.strftime('%Y-%m-%d')==Date:
#     print "Tweeting: ", msg
#     #Actually send the Tweet
#     sendtweet(msg)
# else:
#     print "Data's not fresh."
#     sendtweet("Data for today is not available at this time. Please check http://j.mp/vicpollenalert for today's rating.")
