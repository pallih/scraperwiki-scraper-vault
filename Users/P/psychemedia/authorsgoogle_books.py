import simplejson
import urllib,re
import scraperwiki

i=675

url='http://gdata.youtube.com/feeds/api/videos?v=2&q=authors%40&author=atgoogletalks&alt=json'
#           gdata.youtube.com/feeds/api/videos?v=2&strict=true&start-index=200&q=authors%40&author=atgoogletalks
data=simplejson.load(urllib.urlopen(url))['feed']
print data['openSearch$itemsPerPage']['$t'],data['openSearch$totalResults']['$t'],data

totalResults=data['openSearch$totalResults']['$t']


def getResultsPage(i,data):
    for item in data['entry']:
        #print item['content']['src'],item['title']['$t']
        try:
            author=item['title']['$t'].split(':')[1].strip()
        except: author=item['title']['$t']
        record={'pid':item['id']['$t'],'title':item['title']['$t'],'url':item['content']['src'],'author':author}
        if item['title']['$t'].startswith('Authors@Google'):
            scraperwiki.sqlite.save(["pid"], record)
        i=i+1
    return i

i=getResultsPage(i,data)
while i<totalResults:
    url='http://gdata.youtube.com/feeds/api/videos?v=2&q=authors%40&author=atgoogletalks&start-index='+str(i)+'&alt=json'
    print "Trying:",url
    data=simplejson.load(urllib.urlopen(url))['feed']
    i=getResultsPage(i,data)