#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import datetime
import string
import re

sourcescraper = "Wahltermine"

#defaults
limit = 250
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
sdata = scraperwiki.sqlite.select("* from src.swdata ORDER by date DESC limit ? offset ?", (limit, offset))


#replace key names sanitized for sqlite database with proper xml tag names for meine-demokratie


scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

#print 'offset is ' + str(offset)
#print 'limit is ' + str(limit)

print '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
print '<rss version="2.0" xmlns:md="http://www.meine-demokratie.de">'
print ' <channel>'
print '  <title>%s</title>' % sourcescraper


# items
for item in sdata:
    mynicedate=item['date'].split('-')
    mynicedate=datetime.date(int(mynicedate[0]),int(mynicedate[1]),int(mynicedate[2]))
    mynicedate=mynicedate.strftime('%d.%m.%Y')

    #print [item['parliament']]
    item['parliament'] = re.sub('\xa0','',item['parliament'])

    print "  <item>"
    print "   <md:address>Bundesrepublik Deutschland</md:address>"
    print "   <md:zuordnung>Staat</md:zuordnung>"
    print "   <category>Wahlen</category>"
    print "   <md:tag>Bundestagswahl</md:tag>"
    print "   <md:author>bundeswahlleiter.de</md:author>"
    print "   <pubDate>%s 12:00:00</pubDate>" % item['date']
    print "   <guid>" + item['source'] +"</guid>"
    print "   <%s>%s</%s>" % ('md:start_date',mynicedate,'md:start_date')
    print "   <%s>%s</%s>" % ('md:expiration_date',mynicedate + " 23:59:59",'md:expiration_date')    
    print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum " + str(item['electionnr']) + '. Deutschen Bundestag','title')
    print "   <%s><![CDATA[%s]]></%s>" % ('description','Am ' + mynicedate + ' fand die Wahl zum ' + str(item['electionnr']) + '. Deutschen Bundestag statt.','description')
    print "  </item>"
    
print " </channel>"
print "</rss>"

#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import datetime
import string
import re

sourcescraper = "Wahltermine"

#defaults
limit = 250
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
sdata = scraperwiki.sqlite.select("* from src.swdata ORDER by date DESC limit ? offset ?", (limit, offset))


#replace key names sanitized for sqlite database with proper xml tag names for meine-demokratie


scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

#print 'offset is ' + str(offset)
#print 'limit is ' + str(limit)

print '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
print '<rss version="2.0" xmlns:md="http://www.meine-demokratie.de">'
print ' <channel>'
print '  <title>%s</title>' % sourcescraper


# items
for item in sdata:
    mynicedate=item['date'].split('-')
    mynicedate=datetime.date(int(mynicedate[0]),int(mynicedate[1]),int(mynicedate[2]))
    mynicedate=mynicedate.strftime('%d.%m.%Y')

    #print [item['parliament']]
    item['parliament'] = re.sub('\xa0','',item['parliament'])

    print "  <item>"
    print "   <md:address>Bundesrepublik Deutschland</md:address>"
    print "   <md:zuordnung>Staat</md:zuordnung>"
    print "   <category>Wahlen</category>"
    print "   <md:tag>Bundestagswahl</md:tag>"
    print "   <md:author>bundeswahlleiter.de</md:author>"
    print "   <pubDate>%s 12:00:00</pubDate>" % item['date']
    print "   <guid>" + item['source'] +"</guid>"
    print "   <%s>%s</%s>" % ('md:start_date',mynicedate,'md:start_date')
    print "   <%s>%s</%s>" % ('md:expiration_date',mynicedate + " 23:59:59",'md:expiration_date')    
    print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum " + str(item['electionnr']) + '. Deutschen Bundestag','title')
    print "   <%s><![CDATA[%s]]></%s>" % ('description','Am ' + mynicedate + ' fand die Wahl zum ' + str(item['electionnr']) + '. Deutschen Bundestag statt.','description')
    print "  </item>"
    
print " </channel>"
print "</rss>"

