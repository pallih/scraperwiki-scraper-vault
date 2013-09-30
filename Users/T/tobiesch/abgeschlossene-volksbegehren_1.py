#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import datetime
import string

sourcescraper = "abgeschlossene-volksbegehren"

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
sdata = scraperwiki.sqlite.execute("select * from src.swdata ORDER BY 'Datum VE' DESC limit ? offset ?", (limit, offset))
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
        elif key == 'Initiatoren':
             initiatoren=value
        elif key == 'Erfolg-faktisch':
             erfolg_faktisch=value
        elif key == 'Datum VE':
            mydate=value
            mynicedate=mydate.split('-')
            mynicedate=datetime.date(int(mynicedate[0]),int(mynicedate[1]),int(mynicedate[2]))
            print "   <%s>%s</%s>" % ('md:start_date',value,'md:start_date')
            print "   <%s>%s</%s>" % ('md:expiration_date',value + " 23:59:59",'md:expiration_date')
            print "   <%s>%s</%s>" % ('pubDate',value + " 12:00:00",'pubDate')
        elif key == 'Verfahrenstyp':
            print "   <%s>%s</%s>" % ('md:tag',value,'md:tag')
        elif key == 'Erfolg-formal':
            print "   <%s>%s</%s>" % ('md:tag',value,'md:tag')
        else:
            continue
    print "   <%s><![CDATA[%s]]></%s>" % ('title',mytitle + ' in ' + myaddress,'title')
    print "   <%s><![CDATA[%s]]></%s>" % ('description','Ziel des Volksbegehrens: ' + mytitle+ '<br /><br />Initiatoren: ' + initiatoren + '<br /><br />Datum des Volksentscheides: '+ mynicedate.strftime('%d.%m.%Y') + '<br /><br />Faktischer Erfolg: ' +  erfolg_faktisch,'description')
    print "   <md:address>Bundesland %s</md:address>" % (myaddress)    
    print "   <md:zuordnung>Bundesland</md:zuordnung>"
    print "   <category>Volksbegehren</category>"
    print "   <md:author>mehr-demokratie.de</md:author>"
    print "   <guid>http://www.mehr-demokratie.de/volksentscheid.html#"+myaddress+"-"+string.replace(mytitle,'"','')+"</guid>"
    print "  </item>"
    
print " </channel>"
print "</rss>"

#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import datetime
import string

sourcescraper = "abgeschlossene-volksbegehren"

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
sdata = scraperwiki.sqlite.execute("select * from src.swdata ORDER BY 'Datum VE' DESC limit ? offset ?", (limit, offset))
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
        elif key == 'Initiatoren':
             initiatoren=value
        elif key == 'Erfolg-faktisch':
             erfolg_faktisch=value
        elif key == 'Datum VE':
            mydate=value
            mynicedate=mydate.split('-')
            mynicedate=datetime.date(int(mynicedate[0]),int(mynicedate[1]),int(mynicedate[2]))
            print "   <%s>%s</%s>" % ('md:start_date',value,'md:start_date')
            print "   <%s>%s</%s>" % ('md:expiration_date',value + " 23:59:59",'md:expiration_date')
            print "   <%s>%s</%s>" % ('pubDate',value + " 12:00:00",'pubDate')
        elif key == 'Verfahrenstyp':
            print "   <%s>%s</%s>" % ('md:tag',value,'md:tag')
        elif key == 'Erfolg-formal':
            print "   <%s>%s</%s>" % ('md:tag',value,'md:tag')
        else:
            continue
    print "   <%s><![CDATA[%s]]></%s>" % ('title',mytitle + ' in ' + myaddress,'title')
    print "   <%s><![CDATA[%s]]></%s>" % ('description','Ziel des Volksbegehrens: ' + mytitle+ '<br /><br />Initiatoren: ' + initiatoren + '<br /><br />Datum des Volksentscheides: '+ mynicedate.strftime('%d.%m.%Y') + '<br /><br />Faktischer Erfolg: ' +  erfolg_faktisch,'description')
    print "   <md:address>Bundesland %s</md:address>" % (myaddress)    
    print "   <md:zuordnung>Bundesland</md:zuordnung>"
    print "   <category>Volksbegehren</category>"
    print "   <md:author>mehr-demokratie.de</md:author>"
    print "   <guid>http://www.mehr-demokratie.de/volksentscheid.html#"+myaddress+"-"+string.replace(mytitle,'"','')+"</guid>"
    print "  </item>"
    
print " </channel>"
print "</rss>"

