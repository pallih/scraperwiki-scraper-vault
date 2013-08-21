#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite

sourcescraper = "mdtermine-berlin-de"

#defaults
limit = 500
offset = 0

#URL parameters
params = scraperwiki.utils.GET()
if 'offset' in params:
    offset=int(params['offset'])
if 'limit' in params:
    limit=int(params['limit'])


# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
#get most recently scraped data first
sdata = scraperwiki.sqlite.execute("select * from src.swdata ORDER BY date_scraped DESC limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
items = sdata.get("data")

#replace key names sanitized for sqlite database with proper xml tag names for meine-demokratie
md_keys=[]
for key in keys:
    tempkey=key.replace('md_','md:')
    if tempkey.startswith('md:tag'):
        tempkey='md:tag'
    if tempkey.startswith('category'):
        tempkey='category'
    md_keys.append(tempkey)


scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

#print 'offset is ' + str(offset)
#print 'limit is ' + str(limit)

print '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
print '<rss version="2.0" xmlns:md="http://www.meine-demokratie.de">'
print ' <channel>'
print '  <title>%s</title>' % sourcescraper


# items
for item in items:
    print "  <item>"
    for key, value in zip(md_keys, item):
        if(key=='description'):
            print "   <%s><![CDATA[%s]]></%s>" % (key,value,key)
        else:
            print "   <%s>%s</%s>" % (key,value,key)
    print "  </item>"
    
print " </channel>"
print "</rss>"
