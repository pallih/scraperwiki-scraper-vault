from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from time import strptime, strftime, gmtime
from cgi import escape

sourcescraper = "city-of-ottawa-development-applications"

limit  = 15

print '<?xml version="1.0" encoding="UTF-8" ?>\n'
print ' <rss version="2.0">\n'
print '  <channel>\n'
print '    <title>City of Ottawa Development Applications</title>\n'
print '    <description>Unofficial RSS feed for City of Ottawa Development Applications</description>\n'
print '    <link>http://scraperwiki.com/scrapers/%s/</link>\n' % sourcescraper
print '    <lastBuildDate>%s</lastBuildDate>\n' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <pubDate>%s</pubDate>\n'  % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
 
# rows
current = 0
for row in sorted(getData(sourcescraper, 0, 0), reverse=True, key=lambda row: strptime(row.get('Status_Date'), '%b %d, %Y')):
    current += 1
    if current >= limit:
        break

    title = row.get('Application_Number') + ' - ' + row.get('Primary_Address') + ' - ' + row.get('Review_Status')

    print '    <item>\n'
    print '      <title>%s</title>\n' % title
    print '      <description>%s</description>\n' % row.get('Description')
    print '      <link>%s</link>\n' % escape(row.get('Application_Link'))
    print '      <guid>%s</guid>\n' % row.get('Application_Number')
    print '      <pubDate>%s</pubDate>\n' %  strftime("%a, %d %b %Y %H:%M:%S +0000", strptime(row.get('Status_Date'), '%b %d, %Y'))
    print '    </item>\n'

print ' </channel>\n'
print '</rss> \n'