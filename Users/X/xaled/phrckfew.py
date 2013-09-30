# Blank Python
import scraperwiki
import os,sys
sourcescraper = 'testphrk'

 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('CAST(id as integer) as idd, id, link FROM swdata ORDER BY idd DESC')

print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<title>Phrack.ORG</title>"
print "<link>http://www.phrack.org/</link>"
print "<description>Lastest issues of phrack</description>"

for d in data:
    print "<item>"
    print "<title><![CDATA[Issue num " + d['id'] + "]]></title>"
    print "<link><![CDATA["+d['link']+"]]></link>"
    #print "<guid><![CDATA[" + d['date'] + "]]></guid>"
    #print "<description><![CDATA[" + d['news'] + ")]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"

# Blank Python
import scraperwiki
import os,sys
sourcescraper = 'testphrk'

 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('CAST(id as integer) as idd, id, link FROM swdata ORDER BY idd DESC')

print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<title>Phrack.ORG</title>"
print "<link>http://www.phrack.org/</link>"
print "<description>Lastest issues of phrack</description>"

for d in data:
    print "<item>"
    print "<title><![CDATA[Issue num " + d['id'] + "]]></title>"
    print "<link><![CDATA["+d['link']+"]]></link>"
    #print "<guid><![CDATA[" + d['date'] + "]]></guid>"
    #print "<description><![CDATA[" + d['news'] + ")]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"

