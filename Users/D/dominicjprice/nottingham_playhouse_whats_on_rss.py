import scraperwiki
 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
baseurl = "http://www.nottinghamplayhouse.co.uk/"       

sourcescraper = 'nottingham_playhouse_whats_on'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(           
    '''* from nottingham_playhouse_whats_on.swdata 
    order by \'order\' asc limit 20'''
)
print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<atom:link href=\"https://views.scraperwiki.com/run/nottingham_playhouse_whats_on_rss/\" rel=\"self\" type=\"application/rss+xml\" />"
print "<title>Nottingham Playhouse What's On</title>"
print "<link>" + baseurl + "</link>"
print "<description>What's on information for Nottingham Playhouse</description>"

for d in data:
    print "<item>"
    print "<title><![CDATA[" + d['title'] + "]]></title>"
    print "<link><![CDATA[" + baseurl + d['link'] + "]]></link>"
    print "<guid><![CDATA[" + baseurl + d['link'] + "]]></guid>"
    print "<description><![CDATA[" + d['description'] + "]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"import scraperwiki
 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
baseurl = "http://www.nottinghamplayhouse.co.uk/"       

sourcescraper = 'nottingham_playhouse_whats_on'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(           
    '''* from nottingham_playhouse_whats_on.swdata 
    order by \'order\' asc limit 20'''
)
print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<atom:link href=\"https://views.scraperwiki.com/run/nottingham_playhouse_whats_on_rss/\" rel=\"self\" type=\"application/rss+xml\" />"
print "<title>Nottingham Playhouse What's On</title>"
print "<link>" + baseurl + "</link>"
print "<description>What's on information for Nottingham Playhouse</description>"

for d in data:
    print "<item>"
    print "<title><![CDATA[" + d['title'] + "]]></title>"
    print "<link><![CDATA[" + baseurl + d['link'] + "]]></link>"
    print "<guid><![CDATA[" + baseurl + d['link'] + "]]></guid>"
    print "<description><![CDATA[" + d['description'] + "]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"