# Here we're going to build an RSS feed from the NPIA press release data
# this view is based on the Lincoln Council Committee RSS view
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from time import strptime, strftime, gmtime
from cgi import escape

sourcescraper = 'national-policing-improvement-agency-npia-press-re'

scraperwiki.sqlite.attach('national-policing-improvement-agency-npia-press-re')
print scraperwiki.sqlite.show_tables()           



limit  = 15

print '<?xml version="1.0" encoding="UTF-8" ?>\n'
print ' <rss version="2.0">\n'
print '  <channel>\n'
print '    <title>National Policing Improvement Agency Press Releases</title>\n'
print '    <description>RSS feed for Press Releases from the National Policing Improvement Agency</description>\n'
print '    <link>http://scraperwiki.com/scrapers/%s/</link>\n' % sourcescraper
print '    <lastBuildDate>%s</lastBuildDate>\n' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <pubDate>%s</pubDate>\n'  % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
 
# rows
current = 0
for row in sorted(getData(sourcescraper, 0, 0), reverse=True, key=lambda row: strptime(row.get('date'), '%Y-%m-%d')):
    current += 1
    if current >= limit:
        break

    print '    <item>\n'
    print '      <title>%s</title>\n' % row.get('title')
    print '      <link>%s</link>\n' % escape(row.get('url'))
    print '      <pubDate>%s</pubDate>\n' %  strftime("%a, %d %b %Y %H:%M:%S +0000", strptime(row.get('date'), '%Y-%m-%d'))
    print '    </item>\n'

print ' </channel>\n'
print '</rss> \n'
# Here we're going to build an RSS feed from the NPIA press release data
# this view is based on the Lincoln Council Committee RSS view
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from time import strptime, strftime, gmtime
from cgi import escape

sourcescraper = 'national-policing-improvement-agency-npia-press-re'

scraperwiki.sqlite.attach('national-policing-improvement-agency-npia-press-re')
print scraperwiki.sqlite.show_tables()           



limit  = 15

print '<?xml version="1.0" encoding="UTF-8" ?>\n'
print ' <rss version="2.0">\n'
print '  <channel>\n'
print '    <title>National Policing Improvement Agency Press Releases</title>\n'
print '    <description>RSS feed for Press Releases from the National Policing Improvement Agency</description>\n'
print '    <link>http://scraperwiki.com/scrapers/%s/</link>\n' % sourcescraper
print '    <lastBuildDate>%s</lastBuildDate>\n' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <pubDate>%s</pubDate>\n'  % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
 
# rows
current = 0
for row in sorted(getData(sourcescraper, 0, 0), reverse=True, key=lambda row: strptime(row.get('date'), '%Y-%m-%d')):
    current += 1
    if current >= limit:
        break

    print '    <item>\n'
    print '      <title>%s</title>\n' % row.get('title')
    print '      <link>%s</link>\n' % escape(row.get('url'))
    print '      <pubDate>%s</pubDate>\n' %  strftime("%a, %d %b %Y %H:%M:%S +0000", strptime(row.get('date'), '%Y-%m-%d'))
    print '    </item>\n'

print ' </channel>\n'
print '</rss> \n'
