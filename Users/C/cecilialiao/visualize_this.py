import scraperwiki

# Get max tempearture of London everyday in 2010

import urllib2
from BeautifulSoup import BeautifulSoup
import lxml.html 

for m in range(1,2):
    for d in range(1,32):

        #if(m==2 and d>28):
        #    break
        #elif (m in [4,6,9,11] and d>30):
        #    break

        #timestamp = '2009' + str(m) + str(d)
        #print "Getting data for " + timestamp
        url = "http://www.wunderground.com/history/airport/EGLL/2010/" + str(m) + "/" + str(d) + "/DailyHistory.html,None,100"
        page = urllib2.urlopen(url)
    
        soup = BeautifulSoup(page)
        DailyMaxTemp = soup.findAll(attrs={"class":"nobr"})[3].span.string

        if len(str(m))<2:
            mStamp = '0' + str(m)
        else:
            mStamp = str(m)

        if len(str(d))<2:
            dStamp = '0' + str(d)
        else:
            dStamp = str(d)

        timestamp = '2010' + mStamp + dStamp
        data = {
            'timestamp' : timestamp,
            'MaxDailyTemp' : DailyMaxTemp)
        }
        #print(timestamp + ',' + DailyMaxTemp)
        scraperwiki.sqlite.save(unique_keys=["timestamp"], data=DailyMaxTemp)
