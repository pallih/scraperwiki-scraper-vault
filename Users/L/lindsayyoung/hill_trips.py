import scraperwiki
import lxml.html
import urllib2
import string
import datetime

def read_and_store():
    html = scraperwiki.scrape("http://www.podesta.com/pipeline")
    root = lxml.html.fromstring(html)
    container = root.find_class('stat')
    trips = container[0].text_content()
    oped = container[1].text_content()
    date = str(datetime.datetime.now())
    scraperwiki.sqlite.save(unique_keys=["date"], data={"date":date, "trips":trips, "oped":oped})
    


read_and_store()