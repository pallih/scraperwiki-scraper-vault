import scraperwiki,requests,lxml.html,datetime,urllib,json,re

# Blank Python


def getpage(d,row=0):
    """parse a single search results page; given by a date and a start row."""
    baseurl="http://query.nytimes.com/search/query?frow=%d&n=50&srcht=a&query=&srchst=nyt&submit.x=8&submit.y=10&submit=sub"+\
            "&hdlquery=&bylquery=&daterange=period&mon1=%s&day1=%s&year1=%s&mon2=%s&day2=%s&year2=%s"
    (day,month,year)=d.strftime("%d-%m-%Y").split("-")
    print day,month,year

    modurl=baseurl%(row,day,month,year,day,month,year)

    html=requests.get(modurl).content

    root = lxml.html.fromstring(html)
    urls=[]
    for a in root.cssselect("ol[class='srchSearchResult'] a"):
        url=a.attrib['href']
        if 'query.nytimes.com/gst/fullpage' not in url:
            urls.append(url)
    return urls

def geturls(d):
    """recursively call getpage to get all the search pages"""
    row=0
    urls=[]
    page=getpage(d,row)
    while page:
        urls.extend(page)
        row=row+50
        page=getpage(d,row)
    return urls

def commentspage(url,row=0,retry=0,modurl=''):
    if not modurl:
        baseurl="http://community.nytimes.com/svc/community/V3/requestHandler?"+\
                "&method=get&cmd=GetCommentsAll&url="+\
                "%s&offset=%d"
        niceurl=urllib.quote_plus(urllib.quote_plus(url.partition("?")[0]))
        modurl=baseurl%(niceurl,row)
    print modurl
    data=requests.get(modurl).content[1:-2] # get rid of ( and );
    try:
        assert "DOCTYPE" not in data, 'HTML'
        print data 
        jd=json.loads(data)
        assert jd['status']=="OK", 'ERROR: %s' % str(jd['errors'])
    except AssertionError, e:
        print e
        if retry<5:
            print "Retrying"
            return commentspage(url,row, retry=retry+1)
        else:
            raise
            
    jdata=jd['results']['comments']

    # go through and move replies to base level structure:

    # TODO: if there are more replies than the parent's 'replyCount',
    #       fetch the URL with &commentSequence='commentSequence'

    bail=False
    while not bail:
        print "*"
        bail=True
        for item in jdata:
            if item['replies']:
                if len(item['replies']) == int(item['replyCount']):
                    jdata.extend(item['replies'])
                    item['replies']=[]
                    item['replyCount']=0
                    bail=False
                else: # get more data
                    m='http://community.nytimes.com/svc/community/V3/requestHandler?'+\
                      '&method=get&cmd=GetRepliesBySequence&url='+\
                      '%s&commentSequence=%d' % (niceurl,int(item['commentSequence']))
                    grab=commentspage(url=url, modurl=m)
                    print "Success: ",grab
                    # stick false replies!
                    for g in grab:
                        if not 'replies' in g:
                            g['replies']=[]
                            g['replyCount']=0
                    jdata.extend(grab)
                    item['replies']=[]
                    item['replyCount']=0
                    bail=False
                
    # add additional metadata keys / remove dead items
    for item in jdata:
        item['url']=url.partition("?")[0]
        del item['replyCount']
        del item['replies']

    return jdata
    
def comments(url):    
    """recursively call commentspage to get all the comments"""
    row=0
    page=commentspage(url,row)
    while page:
        scraperwiki.sqlite.save(unique_keys=['commentID'], data=page, table_name='demo')
        print row
        row=row+25
        page=commentspage(url,row)
    
    
d=datetime.date(2012, 1, 1)
#p=geturls(d)
#print len(p)
#print p
comments('http://www.nytimes.com/2012/01/01/us/politics/obama-to-focus-on-congress-and-economy-in-2012-campaign.html?_r=1#commentsContainer')import scraperwiki,requests,lxml.html,datetime,urllib,json,re

# Blank Python


def getpage(d,row=0):
    """parse a single search results page; given by a date and a start row."""
    baseurl="http://query.nytimes.com/search/query?frow=%d&n=50&srcht=a&query=&srchst=nyt&submit.x=8&submit.y=10&submit=sub"+\
            "&hdlquery=&bylquery=&daterange=period&mon1=%s&day1=%s&year1=%s&mon2=%s&day2=%s&year2=%s"
    (day,month,year)=d.strftime("%d-%m-%Y").split("-")
    print day,month,year

    modurl=baseurl%(row,day,month,year,day,month,year)

    html=requests.get(modurl).content

    root = lxml.html.fromstring(html)
    urls=[]
    for a in root.cssselect("ol[class='srchSearchResult'] a"):
        url=a.attrib['href']
        if 'query.nytimes.com/gst/fullpage' not in url:
            urls.append(url)
    return urls

def geturls(d):
    """recursively call getpage to get all the search pages"""
    row=0
    urls=[]
    page=getpage(d,row)
    while page:
        urls.extend(page)
        row=row+50
        page=getpage(d,row)
    return urls

def commentspage(url,row=0,retry=0,modurl=''):
    if not modurl:
        baseurl="http://community.nytimes.com/svc/community/V3/requestHandler?"+\
                "&method=get&cmd=GetCommentsAll&url="+\
                "%s&offset=%d"
        niceurl=urllib.quote_plus(urllib.quote_plus(url.partition("?")[0]))
        modurl=baseurl%(niceurl,row)
    print modurl
    data=requests.get(modurl).content[1:-2] # get rid of ( and );
    try:
        assert "DOCTYPE" not in data, 'HTML'
        print data 
        jd=json.loads(data)
        assert jd['status']=="OK", 'ERROR: %s' % str(jd['errors'])
    except AssertionError, e:
        print e
        if retry<5:
            print "Retrying"
            return commentspage(url,row, retry=retry+1)
        else:
            raise
            
    jdata=jd['results']['comments']

    # go through and move replies to base level structure:

    # TODO: if there are more replies than the parent's 'replyCount',
    #       fetch the URL with &commentSequence='commentSequence'

    bail=False
    while not bail:
        print "*"
        bail=True
        for item in jdata:
            if item['replies']:
                if len(item['replies']) == int(item['replyCount']):
                    jdata.extend(item['replies'])
                    item['replies']=[]
                    item['replyCount']=0
                    bail=False
                else: # get more data
                    m='http://community.nytimes.com/svc/community/V3/requestHandler?'+\
                      '&method=get&cmd=GetRepliesBySequence&url='+\
                      '%s&commentSequence=%d' % (niceurl,int(item['commentSequence']))
                    grab=commentspage(url=url, modurl=m)
                    print "Success: ",grab
                    # stick false replies!
                    for g in grab:
                        if not 'replies' in g:
                            g['replies']=[]
                            g['replyCount']=0
                    jdata.extend(grab)
                    item['replies']=[]
                    item['replyCount']=0
                    bail=False
                
    # add additional metadata keys / remove dead items
    for item in jdata:
        item['url']=url.partition("?")[0]
        del item['replyCount']
        del item['replies']

    return jdata
    
def comments(url):    
    """recursively call commentspage to get all the comments"""
    row=0
    page=commentspage(url,row)
    while page:
        scraperwiki.sqlite.save(unique_keys=['commentID'], data=page, table_name='demo')
        print row
        row=row+25
        page=commentspage(url,row)
    
    
d=datetime.date(2012, 1, 1)
#p=geturls(d)
#print len(p)
#print p
comments('http://www.nytimes.com/2012/01/01/us/politics/obama-to-focus-on-congress-and-economy-in-2012-campaign.html?_r=1#commentsContainer')