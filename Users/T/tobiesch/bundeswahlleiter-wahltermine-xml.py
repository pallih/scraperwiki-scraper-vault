#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import datetime
import string
import re

sourcescraper = "bundeswahlleiter-wahltermine"

sourceurl="http://www.bundeswahlleiter.de/de/kuenftige_wahlen/"

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
sdata = scraperwiki.sqlite.select("* from src.swdata ORDER by startdate DESC limit ? offset ?", (limit, offset))


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
    mynicedate=item['startdate'].split('-')
    mynicedate=datetime.date(int(mynicedate[0]),int(mynicedate[1]),int(mynicedate[2]))
    mynicedate=mynicedate.strftime('%d.%m.%Y')

    print "  <item>"

    #print [item['parliament']]
    if(item['state'] == u'alle Bundesl\xe4nder'):
        if(item['startdate']==item['enddate']):
            mydate="Am " + mynicedate
        else:
            mydate="Im " + item['orig_date'] + ' ' + item['year']            
        print "   <md:address>Bundesrepublik Deutschland</md:address>"
        print "   <md:zuordnung>Staat</md:zuordnung>"
        print "   <md:tag>" + item['electiontype'] + "</md:tag>"            
        if(re.match('.*europa.*',item['electiontype'])):
            print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum Europäischen Parlament",'title')
            print "   <%s><![CDATA[%s]]></%s>" % ('description',mydate + ' findet die Wahl zum Europäischen Parlament statt.','description')
        else:
            print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum Deutschen Bundestag",'title')
            print "   <%s><![CDATA[%s]]></%s>" % ('description',mydate + ' findet die Wahl zum Deutschen Bundestag statt.','description')
    else:
        print "   <md:address>Bundesland " + item['state'] + "</md:address>"
        print "   <md:zuordnung>Bundesland</md:zuordnung>"
        print "   <%s><![CDATA[%s]]></%s>" % ('title',item['electiontype'] + " in " + item['state'],'title')
        if(re.match('.*Landtag.*',item['electiontype'])):
            print "   <md:tag>Landtagswahl</md:tag>"            
        if(re.match('.*Bezirk.*',item['electiontype'])):
            print "   <md:tag>Bezirkswahl</md:tag>"            
        if(re.match('.*Kommunal.*',item['electiontype'])):
            print "   <md:tag>Kommunalwahl</md:tag>" 
        if(re.match('.*Abgeordnetenhaus.*',item['electiontype'])):
            print "   <md:tag>Landtagswahl</md:tag>"
        if(re.match('.*rgerschaft.*',item['electiontype'])):
            print "   <md:tag>Landtagswahl</md:tag>"
        if(item['startdate']==item['enddate']):
            mydate="Am " + mynicedate
        else:
            mydate="Im " + item['orig_date'] + ' ' + item['year']           
        print "   <%s><![CDATA[%s]]></%s>" % ('description',mydate + ' findet in ' + item['state']+ ' die ' + item['electiontype'] +' statt.','description') 

    print "   <category>Wahlen</category>"
    print "   <md:author>bundeswahlleiter.de</md:author>"
    #print "   <pubDate>%s 12:00:00</pubDate>" % item['startdate']

    print "   <guid>" + sourceurl + '#' + item['state'] + '-' + item['year'] + '-' + item['electiontype'] +"</guid>"

    print "   <%s>%s</%s>" % ('md:start_date',item['startdate'],'md:start_date')
    print "   <%s>%s</%s>" % ('md:expiration_date',item['enddate'] + " 23:59:59",'md:expiration_date')    



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

sourcescraper = "bundeswahlleiter-wahltermine"

sourceurl="http://www.bundeswahlleiter.de/de/kuenftige_wahlen/"

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
sdata = scraperwiki.sqlite.select("* from src.swdata ORDER by startdate DESC limit ? offset ?", (limit, offset))


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
    mynicedate=item['startdate'].split('-')
    mynicedate=datetime.date(int(mynicedate[0]),int(mynicedate[1]),int(mynicedate[2]))
    mynicedate=mynicedate.strftime('%d.%m.%Y')

    print "  <item>"

    #print [item['parliament']]
    if(item['state'] == u'alle Bundesl\xe4nder'):
        if(item['startdate']==item['enddate']):
            mydate="Am " + mynicedate
        else:
            mydate="Im " + item['orig_date'] + ' ' + item['year']            
        print "   <md:address>Bundesrepublik Deutschland</md:address>"
        print "   <md:zuordnung>Staat</md:zuordnung>"
        print "   <md:tag>" + item['electiontype'] + "</md:tag>"            
        if(re.match('.*europa.*',item['electiontype'])):
            print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum Europäischen Parlament",'title')
            print "   <%s><![CDATA[%s]]></%s>" % ('description',mydate + ' findet die Wahl zum Europäischen Parlament statt.','description')
        else:
            print "   <%s><![CDATA[%s]]></%s>" % ('title',"Wahl zum Deutschen Bundestag",'title')
            print "   <%s><![CDATA[%s]]></%s>" % ('description',mydate + ' findet die Wahl zum Deutschen Bundestag statt.','description')
    else:
        print "   <md:address>Bundesland " + item['state'] + "</md:address>"
        print "   <md:zuordnung>Bundesland</md:zuordnung>"
        print "   <%s><![CDATA[%s]]></%s>" % ('title',item['electiontype'] + " in " + item['state'],'title')
        if(re.match('.*Landtag.*',item['electiontype'])):
            print "   <md:tag>Landtagswahl</md:tag>"            
        if(re.match('.*Bezirk.*',item['electiontype'])):
            print "   <md:tag>Bezirkswahl</md:tag>"            
        if(re.match('.*Kommunal.*',item['electiontype'])):
            print "   <md:tag>Kommunalwahl</md:tag>" 
        if(re.match('.*Abgeordnetenhaus.*',item['electiontype'])):
            print "   <md:tag>Landtagswahl</md:tag>"
        if(re.match('.*rgerschaft.*',item['electiontype'])):
            print "   <md:tag>Landtagswahl</md:tag>"
        if(item['startdate']==item['enddate']):
            mydate="Am " + mynicedate
        else:
            mydate="Im " + item['orig_date'] + ' ' + item['year']           
        print "   <%s><![CDATA[%s]]></%s>" % ('description',mydate + ' findet in ' + item['state']+ ' die ' + item['electiontype'] +' statt.','description') 

    print "   <category>Wahlen</category>"
    print "   <md:author>bundeswahlleiter.de</md:author>"
    #print "   <pubDate>%s 12:00:00</pubDate>" % item['startdate']

    print "   <guid>" + sourceurl + '#' + item['state'] + '-' + item['year'] + '-' + item['electiontype'] +"</guid>"

    print "   <%s>%s</%s>" % ('md:start_date',item['startdate'],'md:start_date')
    print "   <%s>%s</%s>" % ('md:expiration_date',item['enddate'] + " 23:59:59",'md:expiration_date')    



    print "  </item>"
    
print " </channel>"
print "</rss>"

