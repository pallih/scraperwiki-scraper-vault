import scraperwiki

# Get Page
html = scraperwiki.scrape("http://www.asthma.org.au/PollenAlert.aspx")
import lxml.html           
root = lxml.html.fromstring(html)# turn our HTML into an lxml object

#Get Latest Pollen Rating
LatestRating = root.cssselect("div.div.DnnModule-715") 
print LatestRating         
#print lxml.html.tostring(LatestRating)

###
print LatestRating.text

#Get Date of Latest Pollen Rating

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


LatestRatingDate = root.cssselect("div.ModDNNUserDefinedTableC td")[5]           
DateDirty=lxml.html.tostring(LatestRatingDate)
#print DateDirty
LatestRatingDate =strip_tags(DateDirty)
print LatestRatingDate


#Count Grass & Total Pollen
import re
gcm = root.cssselect("div.ModDNNUserDefinedTableC td")[8]
gcm = gcm.text
#print gcm
match = re.search('([\d]+)[.|/]([\d]+)', gcm)
GrassCount = match.group(1)
TotalCount = match.group(2)

#Convert Dates
import datetime
LatestRatingDate = datetime.datetime.strptime(LatestRatingDate, '%d/%m/%Y').date()

#Save Ratings

scraperwiki.sqlite.save(unique_keys=["Date"], data={"Date":LatestRatingDate, "Rating":LatestRating.text, "GrassCount":GrassCount, "TotalCount":TotalCount})

#record = { "Rating" : LatestRating.text } # column name and value
#scraperwiki.sqlite.save(["Rating"], record) # save the records one by one
#Save Rating Dates
#record = { "Date" : LatestRatingDate } # column name and value
#scraperwiki.sqlite.save(["Date"], record) # save the records one by one