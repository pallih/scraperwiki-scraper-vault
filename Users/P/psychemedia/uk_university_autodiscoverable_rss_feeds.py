import scraperwiki, urllib2,re,mechanize
try: import simplejson as json
except ImportError: import json
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from datetime import datetime


# Load our existing records, so we can persist date_scraped between runs. [via AnnaPS]
DATA_URL = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=uk_university_autodiscoverable_rss_feeds&query=select%20*%20from%20swdata&limit%20100000'
existing_records = urllib2.urlopen(DATA_URL).read()
existing_records = json.loads(existing_records)
#--

def checkPathOnFeedURL(furl,o):
    if furl.startswith('/'):
        x = urlparse(o)
        furl= 'http://'+x.netloc+furl
    return furl

def storeFeedOrNoFeed(hei,dehei,feedcount):
    print 'Feedcount table:',hei,dehei,feedcount
    scraperwiki.sqlite.save(unique_keys=['hei'], table_name="hecountdata", data={'hei':hei,'derefurl':dehei,'feeds':feedcount,'feedyn':(feedcount>0)})

def checkRecord(records,furl):
    for record in records:
        if record['furl']==furl:
            if 'date_first_seen' in record:
                if record['date_first_seen']!=None:
                    return record['date_first_seen']
                else: return datetime.now()
    return datetime.now()

def storeAutoDetectedfeed(fo,hlink,furl,title):
    print 'Using',hlink, furl,title
    dt=''
    dt=checkRecord(existing_records,furl)
    print 'time',dt
    scraperwiki.sqlite.save(unique_keys=['furl'], data={'hei':fo,'feed':title,'furl':furl,'feedHTML':hlink,'date_first_seen':dt})

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
    url='http://query.yahooapis.com/v1/public/yql/psychemedia/feeddetails?url='+urllib2.quote(furl)+'&format=json'
    print "Trying feed url",furl
    try:
        details=json.load(urllib2.urlopen(url))
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

def checkForResponsive(url,derefurl,html):
    lsoup = BeautifulSoup(html)
    metaviewport=lsoup.findAll("meta",{ "name" : "viewport" })
    if len(metaviewport)>0:
        print 'viewport',derefurl
        data={'url':url,'dererfurl':derefurl}
        scraperwiki.sqlite.save(unique_keys=['url'], table_name='viewport', data=data)

def checkForGA(url,derefurl,html):
    #print html
    r=re.match(r".*([Uu][Aa]-\d{4,10}-\d{1,4}).*",html,re.DOTALL)
    #print r
    if r!=None:
        print r.group(1),url,derefurl
        data={'ua':r.group(1),'url':url,'dererfurl':derefurl}
        scraperwiki.sqlite.save(unique_keys=['url'], table_name='gaIDs', data=data)


def getHEIurls():
    heis='http://www.universitiesuk.ac.uk/AboutUs/WhoWeAre/Pages/Members.aspx'
    heis='http://www.universitiesuk.ac.uk/aboutus/members/Pages/default.aspx'
    html = scraperwiki.scrape(heis)

    soup = BeautifulSoup(html)
    urldivs=soup.findAll("div", { "class" : "memberUrl" })

    print urldivs

    urls=[]
    for div in urldivs:
        url=div.a['href']
        print 'trying',url
        #f=urllib2.urlopen(url)
        if url in ['http://www.chiuni.ac.uk/']: continue
        try:
            f=mechanize.urlopen(url)
            derefurl=f.geturl()
            print 'got it'
            #print url,derefurl
            html=f.read()
            checkForGA(url,derefurl,html)
            checkForResponsive(url,derefurl,html)
            urls.append((url,derefurl))
        except: pass
    return urls

def handleURL(url,derefurl):
    adurl='http://query.yahooapis.com/v1/public/yql/psychemedia/feedautodetect?url='+urllib2.quote(url)+'&format=json'
    print adurl
    try:
        data = json.load(urllib2.urlopen(adurl))
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
        storeFeedOrNoFeed(url,derefurl,data['query']['count'])
    except:
        storeFeedOrNoFeed(url,derefurl,0)

urls=getHEIurls()

for url,derefurl in urls:
    handleURL(url,derefurl)

'''
test=['http://www.beds.ac.uk','http://feeds.feedburner.com/uobevents']
test=['http://www.buckingham.ac.uk/','http://www.buckingham.ac.uk/feed/']
handleFeedDetails(test[0],test[1])
'''

