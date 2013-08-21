#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import string

sourcescraper = "laufende_verfahren_auf_landesebene"

#defaults
limit = 50
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
sdata = scraperwiki.sqlite.execute("select * from src.swdata ORDER BY Nr DESC limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
items = sdata.get("data")

#replace key names sanitized for sqlite database with proper xml tag names for meine-demokratie


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
    for key, value in zip(keys, item):
        if key in ('guid','description'):
            print "   <%s><![CDATA[%s]]></%s>" % (key,value,key)
        elif key == 'Titel':
            mytitle=value
        elif key == 'Bundesland':
             myaddress=value           
        elif key == 'Status':
             status=value
        elif key == 'Ziel':
             ziel=value
        elif key == 'Homepage':
             homepage=value
        elif key == 'Verfahrenstyp':
            print "   <%s>%s</%s>" % ('md:tag',value,'md:tag')
        elif key == 'Nr':
             continue
        else:
            print "   <%s>%s</%s>" % (key,value,key)
    print "   <%s><![CDATA[%s]]></%s>" % ('title',mytitle + ' in ' + myaddress,'title')
    print "   <%s><![CDATA[%s]]></%s>" % ('description','Ziel des Volksbegehrens: ' + ziel + '<br /><br />Derzeitiger Stand des Verfahrens: ' + status + '<br /><br />Website der Initiative: <a href="http://'+homepage+'">'+homepage+'</a>' ,'description')
    print "   <md:address>Bundesland %s</md:address>" % (myaddress)    
    print "   <md:zuordnung>Bundesland</md:zuordnung>"
    print "   <category>Volksbegehren</category>"
    print "   <md:author>mehr-demokratie.de</md:author>"
    print "   <guid>http://www.mehr-demokratie.de/volksentscheid.html#"+myaddress+"-"+string.replace(mytitle,'"','')+"</guid>"
    print "  </item>"
    
print " </channel>"
print "</rss>"

