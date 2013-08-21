import scraperwiki

# Blank Python
sourcescraper = 'rss_1'

scraperwiki.sqlite.attach("rss_1")
data = scraperwiki.sqlite.select("* from rss_1.swdata order by added desc")

print "<?xml version='1.0\' encoding='UTF-8'?><rss version='2.0'><channel><title>NZBIndex:'720p'</title><ttl>60</ttl>"           
for d in data:
    print "<item>"
    print "<title>", d["title"], d["year"], "</title>"
    print "<pubDate>", d["pubdate"], "</pubDate>"
    print "<link>",d['imdb'],"</link>"
    print "<description><![CDATA[<p> \
            <a href='",d['imdb'], "' target='_blank'> <img width='150px' src='", d["img"], "'/></a><br/> \
            <strong>Rating:</strong> ", d["rating"], "<br/> \
            <strong>Genre:</strong> ", d["genre"], "<br/> \
            <strong>Description:</strong> ", d["description"], "<br/> \
            <a href='", d["url"], "'>Download</a> \
            </p>]]></description>"
    print "<category>alt.binaries.hdtv.x264</category>"
    print "</item>"
print "</channel></rss>"