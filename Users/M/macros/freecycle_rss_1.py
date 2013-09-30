import scraperwiki
 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
baseurl = "http://www.freecycle.org/"       

sourcescraper = 'freecycle_1'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('* from freecycle_1.swdata order by save_date desc')

print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<title>Freecycle London 'Nintendo' results</title>"
print "<link>" + baseurl + "</link>"
print "<description>All results from Freecycle.org London groups for the keyword 'Nintendo'</description>"

for d in data:
    print "<item>"
    print "<title><![CDATA[" + d['title'] + "]]></title>"
    print "<link><![CDATA[" + d['url'] + "]]></link>"
    print "<guid><![CDATA[" + d['post_id'] + "]]></guid>"
    print "<description><![CDATA[" + d['title'] + " found in group " + d['group'] + " (" + d['group_url'] + ")]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"import scraperwiki
 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
baseurl = "http://www.freecycle.org/"       

sourcescraper = 'freecycle_1'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('* from freecycle_1.swdata order by save_date desc')

print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<title>Freecycle London 'Nintendo' results</title>"
print "<link>" + baseurl + "</link>"
print "<description>All results from Freecycle.org London groups for the keyword 'Nintendo'</description>"

for d in data:
    print "<item>"
    print "<title><![CDATA[" + d['title'] + "]]></title>"
    print "<link><![CDATA[" + d['url'] + "]]></link>"
    print "<guid><![CDATA[" + d['post_id'] + "]]></guid>"
    print "<description><![CDATA[" + d['title'] + " found in group " + d['group'] + " (" + d['group_url'] + ")]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"