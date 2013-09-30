import scraperwiki, simplejson, urllib
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup

def checkPathOnFeedURL(furl,o):
    if furl.startswith('/'):
        x = urlparse(o)
        furl= 'http://'+x.netloc+furl
    return furl

def storeFeedOrNoFeed(hei,feedcount):
    print 'Feedcount table:',hei,feedcount
    scraperwiki.sqlite.save(unique_keys=['hei'], table_name="hecountdata", data={'hei':hei,'feeds':feedcount,'feedyn':(feedcount>0)})

def storeAutoDetectedfeed(fo,hlink,furl,title):
    print 'Using',hlink, furl,title
    scraperwiki.sqlite.save(unique_keys=['furl'], data={'hei':fo,'feed':title,'furl':furl,'feedHTML':hlink})

def handleAcquiredFeedDetail(detail,fo,furl):
    #maybe need to eave this in: http://developer.yahoo.com/yql/console/#h=desc%20feednormalizer
    nocomments=1
    print "Handling",fo,furl,detail
    #fudge this for now - not all feeds declare themselves as alternate - eg aber
    if detail: # or detail['link']['rel']=='alternate':
        if 'content' in detail['title']:
            title=detail['title']['content'].encode('utf-8')
        else:
            title=detail['title'].encode('utf-8')
        hlink=detail['link']['href']
        print title,hlink
        if nocomments==1:
            if not (furl.find('/comments')>-1 or title.startswith('Comments ')):
                storeAutoDetectedfeed(fo,hlink,furl,title)
            else:
                print 'Not using',hlink, furl,title
        else:
            storeAutoDetectedfeed(fo,hlink,furl,title)
    return

def handleFeedDetails(fo,furl):
    url='http://query.yahooapis.com/v1/public/yql/psychemedia/feeddetails?url='+urllib.quote(furl)+'&format=json'
    print "Trying feed url",furl
    try:
        details=simplejson.load(urllib.urlopen(url))
        detail=details['query']['results']['feed']
        print "Acquired",detail
        if type(detail) is list:
            print 'list',detail
            for item in detail:
                handleAcquiredFeedDetail(item,fo,furl)
        else:
            print 'single',detail
            handleAcquiredFeedDetail(detail,fo,furl)
    except:
        pass    




heis='http://jiscinvolve.org/'

html = scraperwiki.scrape(heis)

soup = BeautifulSoup(html)
ul=soup.find("ul", { "class" : "news" })
lis=ul.findAll("li")
print ul

for li in lis:
    url=li.a['href']
    print li,li.a.string,url
    blogname=li.a.string
    feedurl=url+'/wp/feed'
    scraperwiki.sqlite.save(unique_keys=['blogurl'], table_name="jiscblogs", data={'blogurl':url,'blogname':blogname,'feed':feedurl})
    '''
    adurl='http://query.yahooapis.com/v1/public/yql/psychemedia/feedautodetect?url='+urllib.quote(url)+'&format=json'
    print adurl
    try:
        data = simplejson.load(urllib.urlopen(adurl))
        if data['query']['count']>1:
            for item in data['query']['results']['link']:
                furl=checkPathOnFeedURL(item['href'],url)
                print furl,item
                handleFeedDetails(url,furl)
        elif data['query']['count']==1:
            print 'single',data['query']['results']['link']['href']
            furl=checkPathOnFeedURL(data['query']['results']['link']['href'],url)
            print furl
            handleFeedDetails(url,furl)
        else:
            print 'no feed found'
        storeFeedOrNoFeed(url,data['query']['count'])
    except:
        storeFeedOrNoFeed(url,0)
'''
import scraperwiki, simplejson, urllib
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup

def checkPathOnFeedURL(furl,o):
    if furl.startswith('/'):
        x = urlparse(o)
        furl= 'http://'+x.netloc+furl
    return furl

def storeFeedOrNoFeed(hei,feedcount):
    print 'Feedcount table:',hei,feedcount
    scraperwiki.sqlite.save(unique_keys=['hei'], table_name="hecountdata", data={'hei':hei,'feeds':feedcount,'feedyn':(feedcount>0)})

def storeAutoDetectedfeed(fo,hlink,furl,title):
    print 'Using',hlink, furl,title
    scraperwiki.sqlite.save(unique_keys=['furl'], data={'hei':fo,'feed':title,'furl':furl,'feedHTML':hlink})

def handleAcquiredFeedDetail(detail,fo,furl):
    #maybe need to eave this in: http://developer.yahoo.com/yql/console/#h=desc%20feednormalizer
    nocomments=1
    print "Handling",fo,furl,detail
    #fudge this for now - not all feeds declare themselves as alternate - eg aber
    if detail: # or detail['link']['rel']=='alternate':
        if 'content' in detail['title']:
            title=detail['title']['content'].encode('utf-8')
        else:
            title=detail['title'].encode('utf-8')
        hlink=detail['link']['href']
        print title,hlink
        if nocomments==1:
            if not (furl.find('/comments')>-1 or title.startswith('Comments ')):
                storeAutoDetectedfeed(fo,hlink,furl,title)
            else:
                print 'Not using',hlink, furl,title
        else:
            storeAutoDetectedfeed(fo,hlink,furl,title)
    return

def handleFeedDetails(fo,furl):
    url='http://query.yahooapis.com/v1/public/yql/psychemedia/feeddetails?url='+urllib.quote(furl)+'&format=json'
    print "Trying feed url",furl
    try:
        details=simplejson.load(urllib.urlopen(url))
        detail=details['query']['results']['feed']
        print "Acquired",detail
        if type(detail) is list:
            print 'list',detail
            for item in detail:
                handleAcquiredFeedDetail(item,fo,furl)
        else:
            print 'single',detail
            handleAcquiredFeedDetail(detail,fo,furl)
    except:
        pass    




heis='http://jiscinvolve.org/'

html = scraperwiki.scrape(heis)

soup = BeautifulSoup(html)
ul=soup.find("ul", { "class" : "news" })
lis=ul.findAll("li")
print ul

for li in lis:
    url=li.a['href']
    print li,li.a.string,url
    blogname=li.a.string
    feedurl=url+'/wp/feed'
    scraperwiki.sqlite.save(unique_keys=['blogurl'], table_name="jiscblogs", data={'blogurl':url,'blogname':blogname,'feed':feedurl})
    '''
    adurl='http://query.yahooapis.com/v1/public/yql/psychemedia/feedautodetect?url='+urllib.quote(url)+'&format=json'
    print adurl
    try:
        data = simplejson.load(urllib.urlopen(adurl))
        if data['query']['count']>1:
            for item in data['query']['results']['link']:
                furl=checkPathOnFeedURL(item['href'],url)
                print furl,item
                handleFeedDetails(url,furl)
        elif data['query']['count']==1:
            print 'single',data['query']['results']['link']['href']
            furl=checkPathOnFeedURL(data['query']['results']['link']['href'],url)
            print furl
            handleFeedDetails(url,furl)
        else:
            print 'no feed found'
        storeFeedOrNoFeed(url,data['query']['count'])
    except:
        storeFeedOrNoFeed(url,0)
'''
