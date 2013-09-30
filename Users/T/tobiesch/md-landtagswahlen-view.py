#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import datetime
import string
import re

sourcescraper = "landtagswahlen"

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
    print "   <md:address>Bundesland %s</md:address>" % (item['state'])    
    print "   <md:zuordnung>Bundesland</md:zuordnung>"
    print "   <category>Wahlen</category>"
    print "   <md:tag>Landtagswahl</md:tag>"
    print "   <md:tag>%s</md:tag>" % (item['parliament'])
    print "   <md:author>bundeswahlleiter.de</md:author>"
    print "   <pubDate>%s 12:00:00</pubDate>" % item['date']
    print "   <guid>" + item['source'] + "#" + item['date'] +"</guid>"
    print "   <%s>%s</%s>" % ('md:start_date',mynicedate,'md:start_date')
    print "   <%s>%s</%s>" % ('md:expiration_date',mynicedate + " 23:59:59",'md:expiration_date')    

    desc = "   <%s><![CDATA[%s]]></%s>" % ('description','Am ' + mynicedate + ' fand in ' + item['state'] +  ' die Wahl zum ' + str(item['electionnr']) + '. ' + item['parliament'] + ' statt.<br /><br />' + u'Ausf\xfchrliche' + ' Informationen zur Wahl finden Sie auf <a href="http://de.wikipedia.org/wiki/Ergebnisse_der_Landtagswahlen_in_der_Bundesrepublik_Deutschland#' + re.sub('\xfc','.C3.BC',item['parliament'])+ '_in_' + re.sub('\xfc','.C3.BC',item['state']) + '">Wikipedia</a>','description') 
    #print [desc]
    #print [item['parliament']]
    if(item['parliament'] == u'B\xfcrgerschaft'):
        desc=re.sub('zum','zur',desc)
        #desc=re.sub('\xa0 ','',desc)
        #print re.sub('#B\xfc','#BC',desc)
        print desc
        print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zur " + str(item['electionnr']) + '. ' + item['parliament']+ ' in ' + item['state'],'title')
    elif(item['state']=='Saarland'):
        desc = re.sub('_in_S','_im_S',desc)
        desc = re.sub(' in ',' im ',desc)
        print desc
        print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum " + str(item['electionnr']) + '. ' + item['parliament']+ ' im ' + item['state'],'title')
    else:
        print desc
        print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum " + str(item['electionnr']) + '. ' + item['parliament']+ ' in ' + item['state'],'title')
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

sourcescraper = "landtagswahlen"

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
    print "   <md:address>Bundesland %s</md:address>" % (item['state'])    
    print "   <md:zuordnung>Bundesland</md:zuordnung>"
    print "   <category>Wahlen</category>"
    print "   <md:tag>Landtagswahl</md:tag>"
    print "   <md:tag>%s</md:tag>" % (item['parliament'])
    print "   <md:author>bundeswahlleiter.de</md:author>"
    print "   <pubDate>%s 12:00:00</pubDate>" % item['date']
    print "   <guid>" + item['source'] + "#" + item['date'] +"</guid>"
    print "   <%s>%s</%s>" % ('md:start_date',mynicedate,'md:start_date')
    print "   <%s>%s</%s>" % ('md:expiration_date',mynicedate + " 23:59:59",'md:expiration_date')    

    desc = "   <%s><![CDATA[%s]]></%s>" % ('description','Am ' + mynicedate + ' fand in ' + item['state'] +  ' die Wahl zum ' + str(item['electionnr']) + '. ' + item['parliament'] + ' statt.<br /><br />' + u'Ausf\xfchrliche' + ' Informationen zur Wahl finden Sie auf <a href="http://de.wikipedia.org/wiki/Ergebnisse_der_Landtagswahlen_in_der_Bundesrepublik_Deutschland#' + re.sub('\xfc','.C3.BC',item['parliament'])+ '_in_' + re.sub('\xfc','.C3.BC',item['state']) + '">Wikipedia</a>','description') 
    #print [desc]
    #print [item['parliament']]
    if(item['parliament'] == u'B\xfcrgerschaft'):
        desc=re.sub('zum','zur',desc)
        #desc=re.sub('\xa0 ','',desc)
        #print re.sub('#B\xfc','#BC',desc)
        print desc
        print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zur " + str(item['electionnr']) + '. ' + item['parliament']+ ' in ' + item['state'],'title')
    elif(item['state']=='Saarland'):
        desc = re.sub('_in_S','_im_S',desc)
        desc = re.sub(' in ',' im ',desc)
        print desc
        print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum " + str(item['electionnr']) + '. ' + item['parliament']+ ' im ' + item['state'],'title')
    else:
        print desc
        print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum " + str(item['electionnr']) + '. ' + item['parliament']+ ' in ' + item['state'],'title')
    print "  </item>"
    
print " </channel>"
print "</rss>"

