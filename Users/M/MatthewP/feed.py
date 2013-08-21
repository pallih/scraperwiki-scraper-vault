#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import re

sourcescraper = "swale-democratic-services-events-diary"

limit = 30
offset = 0

keys = getKeys(sourcescraper)
data = getData(sourcescraper, 1, offset)

#res
ure = re.compile(".*(http.*uid=[0-9]*)", re.DOTALL)
nre = re.compile(".*strong.(.*strong)", re.DOTALL) 
allre = re.compile(".*", re.DOTALL)

#meta
for row in getData(sourcescraper, limit, offset):
    updated = "%s%s" % (row.get('datetime'), "Z")
    break

print """<?xml version="1.0" encoding="utf-8"?>

<feed xmlns='http://www.w3.org/2005/Atom'>
    <title type='text'>Swale Democratic Services Calendar</title>
    <subtitle type='html'>Open Swale</subtitle>
    <updated>%s</updated>
    <id>http://scraperwikiviews.com/run/feed/?</id>
    <link rel='self' type='application/atom+xml' href='http://scraperwikiviews.com/run/feed/?'/>
    <rights>CC-by</rights>
    <generator uri='http://scraperwikiviews.com/run/feed/?' version='1.0'>ScraperWiki view - matthew@refute.me.uk</generator>""" % (updated)

# rows
for row in getData(sourcescraper, limit, offset):
    try:
        committee = row.get('committee')
        committee_uri = re.match(ure, committee).group(1)
        committee_name = re.match(nre, committee).group(1)[:-8]
        date = row.get('date')
        time = row.get('time')
        venue = row.get('venue')
        id = row.get('unique')
        updated = "%s%s" % (row.get('datetime'), "Z")
        printable = 1
    except:
        printable = 0

    if printable == 1: 
        print """    <entry>
        <title> %s </title>
        <link href='%s'/>
        <id>%s</id>
        <updated>%s</updated> 
        <summary type='html'>
        <![CDATA[
            %s <p/> %s - %s </p> %s 
        ]]>
        </summary>
        <author>
            <name>Open Swale</name>
            <uri>http://scraperwiki.com/scrapers/swale-democratic-services-events-diary/</uri>
            <email>matthew@refute.me.uk</email>
        </author>
    </entry>""" % (committee_name, committee_uri, committee_uri, updated, committee, date, time, venue)

print "</feed>"