import scraperwiki
import lxml.html
import urllib2
import simplejson
import datetime

url = "http://www3.septa.org/hackathon/TrainView/"
json = urllib2.urlopen(url).read()

(true, false, null) = (True, False, None)
trainstatus = eval(json)

trains = len(trainstatus)

for train in trainstatus:
    train["datetime"] = datetime.datetime.now()



for k in range(0, trains):
    scraperwiki.sqlite.save(unique_keys = ["trainno"], data=trainstatus[k])

#print datetime.datetime.now()
import scraperwiki
import lxml.html
import urllib2
import simplejson
import datetime

url = "http://www3.septa.org/hackathon/TrainView/"
json = urllib2.urlopen(url).read()

(true, false, null) = (True, False, None)
trainstatus = eval(json)

trains = len(trainstatus)

for train in trainstatus:
    train["datetime"] = datetime.datetime.now()



for k in range(0, trains):
    scraperwiki.sqlite.save(unique_keys = ["trainno"], data=trainstatus[k])

#print datetime.datetime.now()
