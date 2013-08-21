from cgi import escape
from time import strftime, gmtime
from datetime import datetime
import scraperwiki

sourcescraper = "city_of_ottawa_development_applications"

limit  = 15

scraperwiki.utils.httpresponseheader('Content-Type', 'application/rss_xml')

print '<?xml version="1.0" encoding="UTF-8" ?>\n'
print ' <rss version="2.0">\n'
print '  <channel>\n'
print '    <title>City of Ottawa Development Applications</title>\n'
print '    <description>Unofficial RSS feed for City of Ottawa Development Applications</description>\n'
print '    <link>http://scraperwiki.com/scrapers/%s/</link>\n' % sourcescraper
print '    <lastBuildDate>%s</lastBuildDate>\n' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <pubDate>%s</pubDate>\n'  % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
 
# rows

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(           
    "DISTINCT * FROM %s.Applications AS App, %s.Locations AS Loc ON App.Application_Number=Loc.Application_Number WHERE Current=1 OR App.Application_Number='D01-01-08-0007' ORDER BY App.Last_Scrape LIMIT 300" % (sourcescraper, sourcescraper)
)

# compute the changes
## get the changed items
ids = []
for r in data:
    ids.append("Application_Number='" + r['Application_Number'] + "'")


prev = scraperwiki.sqlite.select(           
    "*, MAX(Last_Scrape) FROM %s.Applications WHERE Current=0 AND (%s) GROUP BY Application_Number ORDER BY Last_Scrape" % (sourcescraper, " OR ".join(ids))
)

prevById = {}
for r in prev:
    prevById[r['Application_Number']] = r

def application_diff(pair):
    book_keeping_fields = {'Last_Scrape' : 0, 'Date_Status' : 0, 'Application_URI' : 0, 'Status_Hash' : 0}
    diff = {}
    for k in pair[0].keys():
        if book_keeping_fields.has_key(k):
            continue

        try:
            if pair[0][k] != pair[1][k]:
                diff[k] = [pair[0][k], pair[1][k]]
        except KeyError:
            continue # We get these when we have columns in pair[0] that don't exist in p[1] due to joins.

    return diff

def stringify_diff(d):
    out = "<table border='1' width='100%'>"
    for k in d.keys():
        out += '''<tr><td rowspan="2" valign="top">%s</td><td>%s</td></tr><tr><td><strike>%s</strike></td></tr>''' % (escape(k), escape(d[k][0]), escape(d[k][1]))

    out += "</table>"
    return out


#print data
for row in data:
    title = "%s - %s" % (row['Address'], row['Application_Number'])

    c = "<b>Newly added.</b>"
    if prevById.has_key(row['Application_Number']):
        c = "<b>Changes</b><p/>" + stringify_diff(application_diff([row, prevById[row['Application_Number']]]))


    print '    <item>\n'
    print '      <title>%s</title>\n' % escape(title)
    print '      <description>%s&lt;p/&gt;%s</description>\n' % (escape(row['Description']), escape(c))
    print '      <link>%s</link>\n' % escape(row['Application_URI'])
    print '      <guid>%s</guid>\n' % escape(row['Application_Number'])
    print '      <pubDate>%s</pubDate>\n' %  escape(datetime.fromtimestamp(row['Last_Scrape']).strftime("%a, %d %b %Y %H:%M:%S +0000"))
    print '    </item>\n'

print ' </channel>\n'
print '</rss> \n'