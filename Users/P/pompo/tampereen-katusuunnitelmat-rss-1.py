from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from time import strptime, strftime, gmtime
sourcescraper = 'tampereen-katusuunnitelmat'


limit = 0
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

print '<?xml version="1.0"?>\n'
print '<rss version="2.0">\n'
print ' <channel>\n'
print '  <title>Tampereen kaupungin katusuunnitelmat</title>\n'
print '  <link>http://www.tampere.fi/liikennejakadut/katusuunnitelmat.html</link>\n'
print '  <description>Katusuunnitelmat</description>\n'
print '  <language>fi-fi</language>\n'

# rows
for row in getData(sourcescraper, limit, offset):
    print '  <item>\n',
    print '   <title>%s</title>\n' % row.get('date'),
    print '   <link>%s</link>\n' % row.get('url'),
    print '   <guid>%s</guid>\n' % row.get('guid'),
    print '   <description>%s</description>\n' % row.get('titles'),
    print "  </item>\n"
    
print ' </channel>\n'
print '</rss>\n'
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from time import strptime, strftime, gmtime
sourcescraper = 'tampereen-katusuunnitelmat'


limit = 0
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

print '<?xml version="1.0"?>\n'
print '<rss version="2.0">\n'
print ' <channel>\n'
print '  <title>Tampereen kaupungin katusuunnitelmat</title>\n'
print '  <link>http://www.tampere.fi/liikennejakadut/katusuunnitelmat.html</link>\n'
print '  <description>Katusuunnitelmat</description>\n'
print '  <language>fi-fi</language>\n'

# rows
for row in getData(sourcescraper, limit, offset):
    print '  <item>\n',
    print '   <title>%s</title>\n' % row.get('date'),
    print '   <link>%s</link>\n' % row.get('url'),
    print '   <guid>%s</guid>\n' % row.get('guid'),
    print '   <description>%s</description>\n' % row.get('titles'),
    print "  </item>\n"
    
print ' </channel>\n'
print '</rss>\n'
