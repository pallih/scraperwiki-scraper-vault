import scraperwiki           
import lxml.html     


quickfix=0 #allows us to start checking for feeds some way down the page...

#--------
import urllib,simplejson
from urlparse import urlparse

def checkPathOnFeedURL(furl,o):
    if furl.startswith('/'):
        x = urlparse(o)
        furl= 'http://'+x.netloc+furl
    return furl

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


#--------

def doit(url):
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
                else: print 'no feed found'
            except:
                pass




url="http://brodiesnotes.blogspot.com/2009/07/amrc-member-charities-websites.html"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

div=root.cssselect('div[class="post-body entry-content"]')

c=0
for i in div[0][-2]:
    anchors=i.cssselect('a')
    for a in anchors:
        if 'href' in a.attrib:
            url=a.attrib['href']
            c=c+1
            print c,url

            if c>quickfix:
                doit(url)


import scraperwiki           
import lxml.html     


quickfix=0 #allows us to start checking for feeds some way down the page...

#--------
import urllib,simplejson
from urlparse import urlparse

def checkPathOnFeedURL(furl,o):
    if furl.startswith('/'):
        x = urlparse(o)
        furl= 'http://'+x.netloc+furl
    return furl

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


#--------

def doit(url):
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
                else: print 'no feed found'
            except:
                pass




url="http://brodiesnotes.blogspot.com/2009/07/amrc-member-charities-websites.html"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

div=root.cssselect('div[class="post-body entry-content"]')

c=0
for i in div[0][-2]:
    anchors=i.cssselect('a')
    for a in anchors:
        if 'href' in a.attrib:
            url=a.attrib['href']
            c=c+1
            print c,url

            if c>quickfix:
                doit(url)


