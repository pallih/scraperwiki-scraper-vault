import simplejson
import urllib,re
import scraperwiki
import sys

def getResultsPage(url,data):
    for item in data['entry']:
        try:
            author=item['title']['$t'].split(':')[1].strip()
        except: author=item['title']['$t']
        try:
            itemurl = item['content']['src']
        except: itemurl = item['link'][0]['href']
        record={'pid':item['id']['$t'],'title':item['title']['$t'],'url':itemurl,'author':author}
        if item['title']['$t'].startswith('Authors@Google'):
            scraperwiki.sqlite.save(["pid"], record)
    nxt = [q["href"] for q in data["link"] if q["rel"] == u'next']
    if len(nxt) > 0:
        url = nxt[0]
        scraperwiki.sqlite.save_var("url", url)
    else:
        url = None
        scraperwiki.sqlite.save_var("url", "FINISHED")
    return url

url = scraperwiki.sqlite.get_var("url",'http://gdata.youtube.com/feeds/api/videos?v=2&q=authors%40&author=atgoogletalks&alt=json')
print "Next URL = ", url

if url == "FINISHED":
    sys.exit("Done!")

data=simplejson.load(urllib.urlopen(url))['feed']

#print data['openSearch$itemsPerPage']['$t'],data['openSearch$totalResults']['$t'],data

#totalResults=data['openSearch$totalResults']['$t']
url = getResultsPage(url,data)
while (url):
    print "Trying:",url
    data=simplejson.load(urllib.urlopen(url))['feed']
    url = getResultsPage(url,data)
import simplejson
import urllib,re
import scraperwiki
import sys

def getResultsPage(url,data):
    for item in data['entry']:
        try:
            author=item['title']['$t'].split(':')[1].strip()
        except: author=item['title']['$t']
        try:
            itemurl = item['content']['src']
        except: itemurl = item['link'][0]['href']
        record={'pid':item['id']['$t'],'title':item['title']['$t'],'url':itemurl,'author':author}
        if item['title']['$t'].startswith('Authors@Google'):
            scraperwiki.sqlite.save(["pid"], record)
    nxt = [q["href"] for q in data["link"] if q["rel"] == u'next']
    if len(nxt) > 0:
        url = nxt[0]
        scraperwiki.sqlite.save_var("url", url)
    else:
        url = None
        scraperwiki.sqlite.save_var("url", "FINISHED")
    return url

url = scraperwiki.sqlite.get_var("url",'http://gdata.youtube.com/feeds/api/videos?v=2&q=authors%40&author=atgoogletalks&alt=json')
print "Next URL = ", url

if url == "FINISHED":
    sys.exit("Done!")

data=simplejson.load(urllib.urlopen(url))['feed']

#print data['openSearch$itemsPerPage']['$t'],data['openSearch$totalResults']['$t'],data

#totalResults=data['openSearch$totalResults']['$t']
url = getResultsPage(url,data)
while (url):
    print "Trying:",url
    data=simplejson.load(urllib.urlopen(url))['feed']
    url = getResultsPage(url,data)
