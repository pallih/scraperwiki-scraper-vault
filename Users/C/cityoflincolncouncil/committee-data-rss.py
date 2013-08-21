# Here we're going to build an RSS feed from our Committee Data
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from time import strptime, strftime, gmtime
from cgi import escape

sourcescraper = 'city-of-lincoln-council-committee-updates-rss-feed'

limit  = 15

print '<?xml version="1.0" encoding="UTF-8" ?>\n'
print ' <rss version="2.0">\n'
print '  <channel>\n'
print '    <title>City of Lincoln Council Committee Updates</title>\n'
print '    <description>RSS feed for Monthly Committee Updates from the City of Lincoln Council</description>\n'
print '    <link>http://scraperwiki.com/scrapers/%s/</link>\n' % sourcescraper
print '    <lastBuildDate>%s</lastBuildDate>\n' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <pubDate>%s</pubDate>\n'  % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
 
# rows
current = 0
for row in sorted(getData(sourcescraper, 0, 0), reverse=True, key=lambda row: strptime(row.get('Date'), '%d %B %Y')):
    current += 1
    if current >= limit:
        break

    print '    <item>\n'
    print '      <title>%s</title>\n' % row.get('Title')
    print '      <description>%s</description>\n' % row.get('Event')
    print '      <link>%s</link>\n' % escape(row.get('Link'))
    print '      <pubDate>%s</pubDate>\n' %  strftime("%a, %d %b %Y %H:%M:%S +0000", strptime(row.get('Date'), '%d %B %Y'))
    print '    </item>\n'

print ' </channel>\n'
print '</rss> \n'