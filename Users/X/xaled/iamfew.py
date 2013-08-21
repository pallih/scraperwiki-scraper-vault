# Blank Python
import scraperwiki
import os,sys
sourcescraper = 'testiam'

 
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select('* FROM promo ORDER BY time DESC')

print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
print "<channel>"
print "<title>PROMO IAM</title>"
print "<link>http://www.iam.ma/PROMO/Pages/promo.aspx</link>"
print "<description>PROMO MAROC TELECOM</description>"
link ="http://www.iam.ma/PROMO/Pages/promo.aspx"

for d in data:
    print "<item>"
    print "<title><![CDATA[" + d['title'] + "]]></title>"
    print "<link><![CDATA["+link+"#"+d['hash']+"]]></link>"
    #print "<guid><![CDATA[" + d['date'] + "]]></guid>"
    print "<description><![CDATA[" + d['content'] + ")]]></description>"
    print "</item>"

print "</channel>"
print "</rss>"

