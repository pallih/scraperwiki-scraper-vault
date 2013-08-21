import scraperwiki
import BeautifulSoup
import urllib2, datetime, sys
from urllib2 import HTTPError
from scraperwiki import datastore

#scrape page
for id in range(8590000,8596057):
    url = 'http://news.bbc.co.uk/1/hi/%s.stm' %(id,)
    
    try:
        request = urllib2.urlopen(url)
    except HTTPError,e :
        if (e.code ==404):
            #Should cache these ids and exclude them from the range on a rerun
            print 'Not Found: %s' %(url)
        continue
    
    html = request.read()
    
    #Would have been nice for conditional processing!
    #etag = request.headers['etag']
    
    page = BeautifulSoup.BeautifulSoup(html)
    
    try:
        headline = page.head('meta',{'name':'Headline'})[0]['content']
        description = page.head('meta',{'name':'Description'})[0]['content']
        publication_date = page.head('meta',{'name':'OriginalPublicationDate'})[0]['content']
    
        date = datetime.datetime.strptime(publication_date, "%Y/%m/%d %H:%M:%S")
    
        datastore.save(['id'],{'id':id, 'url':url, 'headline':headline,'description':description,'publication_date':publication_date},date)
    except:
        print "Unexpected error:", sys.exc_info()[0]


