import scraperwiki,requests,lxml.html
# Blank Python

url='http://soccernet.espn.go.com/commentary?id=318101&cc=5739'
scraperwiki.sqlite.attach('prem-waler', 'prem-walker') # damn typos!

def createtable():
    schema="""CREATE TABLE `prem` (`url` text, `content` text, `image` text, `time` integer, Primary key (url,content,image,time))"""
    scraperwiki.sqlite.execute(schema)

def getcomm(li):
    comm=li.cssselect("div[class='comment']")
    if len(comm)>0: return comm[0]
    comm=li.cssselect("div[class='comment ']")
    if len(comm)>0: return comm[0]
    comm=li.cssselect("div[class='comment  select-comment']")
    if len(comm)>0: return comm[0]
    print "Can't find comment in string"
    litext=lxml.html.tostring(li)
    print litext
    scraperwiki.sqlite.save(unique_keys=['url'], data={'url':url,'exception':None,'where':'li','text':litext}, table_name='error')
    raise

def scrapeurl(url):
    html=requests.get(url).content
    root = lxml.html.fromstring(html)
    
    # metadata handler
    meta={}
    meta['home']=root.cssselect("div[class='team home']")[0].text_content()
    meta['away']=root.cssselect("div[class='team away']")[0].text_content()
    meta['score']=root.cssselect("p[class='matchup-score']")[0].text_content()
    meta['when']=root.cssselect("div[class='game-time-location'] p")[1].text_content()
    meta['where']=root.cssselect("div[class='game-time-location'] p")[2].text_content()
    meta['url']=url
    scraperwiki.sqlite.save(unique_keys=['url'], data=meta, table_name='meta')

    if 'P' in meta['score']: # skip postponed matches
        print "Skipped; postponed"
        return
    
    # comments handler
    for li in root.cssselect("ul[id='convo-list'] li"):
        data={'url':url}
        t=li.cssselect("div[class='timestamp']")[0].text_content()
    
        try:
            data['time']=int(t.replace("'",'').replace('\n',''))
        except ValueError: # prob blank
            assert t==u'\xa0\n' or t=='-'

        comm=getcomm(li)
        data['content']=comm.text_content()

        try:
            data['image']=comm.cssselect("img")[0].attrib['src']
        except IndexError:
            pass # clearly no image provided
        #print data
        scraperwiki.sqlite.save(unique_keys=[], data=data, table_name='prem')

def url2url(url):
    return "http://soccernet.espn.go.com/commentary?id=%s" % url.split('/')[-1]

def nexturl(baseurl):
    return scraperwiki.sqlite.select("min(url) from `prem-walker` where url>?", baseurl)[0]['min(url)']


walker = scraperwiki.utils.swimport('prem-waler')

recent=walker.scrapeurlw('http://soccernet.espn.go.com/results/_/league/eng.1/barclays-premier-league', saver=False)
for baseurl in recent:
    print baseurl['url']
    u=url2url(baseurl['url'])
    print u
    scrapeurl(u)
    


exit()

# The following code was used to populate the tables the first time.
# Create Table with primary key = all columns
try:
    createtable()
except Exception, e:
    print "Table exists? ",e

# Get first page or page we were up to
baseurl=scraperwiki.sqlite.get_var('next')
#baseurl=scraperwiki.sqlite.select("min(url) from `prem-walker`")[0]['min(url)']
#baseurl='http://soccernet.espn.go.com/commentary?id=178182' # monkeypatch

while baseurl:
    u=url2url(baseurl)
    print u
    scrapeurl(u)
    baseurl=nexturl(baseurl)
    scraperwiki.sqlite.save_var('next',baseurl)import scraperwiki,requests,lxml.html
# Blank Python

url='http://soccernet.espn.go.com/commentary?id=318101&cc=5739'
scraperwiki.sqlite.attach('prem-waler', 'prem-walker') # damn typos!

def createtable():
    schema="""CREATE TABLE `prem` (`url` text, `content` text, `image` text, `time` integer, Primary key (url,content,image,time))"""
    scraperwiki.sqlite.execute(schema)

def getcomm(li):
    comm=li.cssselect("div[class='comment']")
    if len(comm)>0: return comm[0]
    comm=li.cssselect("div[class='comment ']")
    if len(comm)>0: return comm[0]
    comm=li.cssselect("div[class='comment  select-comment']")
    if len(comm)>0: return comm[0]
    print "Can't find comment in string"
    litext=lxml.html.tostring(li)
    print litext
    scraperwiki.sqlite.save(unique_keys=['url'], data={'url':url,'exception':None,'where':'li','text':litext}, table_name='error')
    raise

def scrapeurl(url):
    html=requests.get(url).content
    root = lxml.html.fromstring(html)
    
    # metadata handler
    meta={}
    meta['home']=root.cssselect("div[class='team home']")[0].text_content()
    meta['away']=root.cssselect("div[class='team away']")[0].text_content()
    meta['score']=root.cssselect("p[class='matchup-score']")[0].text_content()
    meta['when']=root.cssselect("div[class='game-time-location'] p")[1].text_content()
    meta['where']=root.cssselect("div[class='game-time-location'] p")[2].text_content()
    meta['url']=url
    scraperwiki.sqlite.save(unique_keys=['url'], data=meta, table_name='meta')

    if 'P' in meta['score']: # skip postponed matches
        print "Skipped; postponed"
        return
    
    # comments handler
    for li in root.cssselect("ul[id='convo-list'] li"):
        data={'url':url}
        t=li.cssselect("div[class='timestamp']")[0].text_content()
    
        try:
            data['time']=int(t.replace("'",'').replace('\n',''))
        except ValueError: # prob blank
            assert t==u'\xa0\n' or t=='-'

        comm=getcomm(li)
        data['content']=comm.text_content()

        try:
            data['image']=comm.cssselect("img")[0].attrib['src']
        except IndexError:
            pass # clearly no image provided
        #print data
        scraperwiki.sqlite.save(unique_keys=[], data=data, table_name='prem')

def url2url(url):
    return "http://soccernet.espn.go.com/commentary?id=%s" % url.split('/')[-1]

def nexturl(baseurl):
    return scraperwiki.sqlite.select("min(url) from `prem-walker` where url>?", baseurl)[0]['min(url)']


walker = scraperwiki.utils.swimport('prem-waler')

recent=walker.scrapeurlw('http://soccernet.espn.go.com/results/_/league/eng.1/barclays-premier-league', saver=False)
for baseurl in recent:
    print baseurl['url']
    u=url2url(baseurl['url'])
    print u
    scrapeurl(u)
    


exit()

# The following code was used to populate the tables the first time.
# Create Table with primary key = all columns
try:
    createtable()
except Exception, e:
    print "Table exists? ",e

# Get first page or page we were up to
baseurl=scraperwiki.sqlite.get_var('next')
#baseurl=scraperwiki.sqlite.select("min(url) from `prem-walker`")[0]['min(url)']
#baseurl='http://soccernet.espn.go.com/commentary?id=178182' # monkeypatch

while baseurl:
    u=url2url(baseurl)
    print u
    scrapeurl(u)
    baseurl=nexturl(baseurl)
    scraperwiki.sqlite.save_var('next',baseurl)