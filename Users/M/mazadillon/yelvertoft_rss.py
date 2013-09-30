import scraperwiki
 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
baseurl = "http://www.yelertoftchurch.org.uk/"       

sourcescraper = 'yelvertoft_scraper'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('* from yelvertoft_scraper.swdata order by date desc')

print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<title>Yelvertoft Church</title>"
print "<link>" + baseurl + "</link>"
print "<description>Latest news from Yelvertoft Church</description>"

for d in data:
    print "<item>"
    print "<title><![CDATA[News From " + d['date'] + "]]></title>"
    print "<link><![CDATA[http://www.yelvertoftchurch.org.uk/]]></link>"
    print "<guid><![CDATA[" + d['date'] + "]]></guid>"
    print "<description><![CDATA[" + d['news'] + ")]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"import scraperwiki
 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
baseurl = "http://www.yelertoftchurch.org.uk/"       

sourcescraper = 'yelvertoft_scraper'
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('* from yelvertoft_scraper.swdata order by date desc')

print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<title>Yelvertoft Church</title>"
print "<link>" + baseurl + "</link>"
print "<description>Latest news from Yelvertoft Church</description>"

for d in data:
    print "<item>"
    print "<title><![CDATA[News From " + d['date'] + "]]></title>"
    print "<link><![CDATA[http://www.yelvertoftchurch.org.uk/]]></link>"
    print "<guid><![CDATA[" + d['date'] + "]]></guid>"
    print "<description><![CDATA[" + d['news'] + ")]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"