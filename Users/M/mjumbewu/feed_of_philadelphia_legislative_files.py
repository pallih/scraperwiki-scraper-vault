# This feed was validated by http://feedvalidator.org/

import scraperwiki
from scraperwiki import utils
from time import strptime, strftime, gmtime
from cgi import escape

# It's an RSS feed, so serve it as such
utils.httpresponseheader("Content-Type", "application/rss+xml")
#scraperwiki.dumpMessage({'message_type': 'httpresponseheader', 'headerkey': "Content-Type", 'headervalue': "application/rss+xml"})

sourcescraper = 'philadelphia_legislative_files'
view = 'feed_of_philadelphia_legislative_files'


print '<?xml version="1.0" encoding="UTF-8" ?>'
print
print ' <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">'
print '  <channel>'
print '    <title>Philadelphia Legislative Documents</title>'
print '    <description>RSS feed of new Philadelphia legislative documents. Search through the documents at http://legislation.phila.gov/. Do even more with the data at http://scraperwiki.com/scrapers/philadelphia_legislative_files/.</description>'
print '    <link>http://scraperwiki.com/scrapers/%s/</link>' % sourcescraper
#print '    <lastBuildDate>%s</lastBuildDate>\n' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <pubDate>%s</pubDate>'  % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <atom:link href="http://scraperwikiviews.com/run/%s/" rel="self" type="application/rss+xml" />' % view

# rows
scraperwiki.sqlite.attach('philadelphia_legislative_files')
rows = scraperwiki.sqlite.select('* from `philadelphia_legislative_files`.swdata')

# Since I did not store the dates as datetime fields in the database, I have to 
# do it here.  This is not efficient, and in the long term dates should be stored
# in a reasonable format.
def row_date(row):
    date_str = row.get('intro_date')
    if '/' in date_str:
        return strptime(date_str, '%m/%d/%Y')
    elif 'T' in date_str:
        return strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    else:
        return strptime(date_str, '%Y-%m-%d')

rows = sorted(rows, reverse=True, key=row_date)

more_allowed  = 1000
for row in rows:
    if not more_allowed:
        break

    print '    <item>'
    print '      <title>%s</title>' % row.get('title')
    print '      <link>%s</link>' % escape(row.get('url'))
    print '      <guid>%s</guid>' % escape(row.get('url'))
    print '      <description>The %s introduced by %s is currently %s.</description>' % (row.get('type'), row.get('sponsors'), row.get('status'))
    print '      <pubDate>%s</pubDate>' %  strftime("%a, %d %b %Y %H:%M:%S +0000", row_date(row))
    print '    </item>'
    more_allowed -= 1

print ' </channel>'
print '</rss> '
# This feed was validated by http://feedvalidator.org/

import scraperwiki
from scraperwiki import utils
from time import strptime, strftime, gmtime
from cgi import escape

# It's an RSS feed, so serve it as such
utils.httpresponseheader("Content-Type", "application/rss+xml")
#scraperwiki.dumpMessage({'message_type': 'httpresponseheader', 'headerkey': "Content-Type", 'headervalue': "application/rss+xml"})

sourcescraper = 'philadelphia_legislative_files'
view = 'feed_of_philadelphia_legislative_files'


print '<?xml version="1.0" encoding="UTF-8" ?>'
print
print ' <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">'
print '  <channel>'
print '    <title>Philadelphia Legislative Documents</title>'
print '    <description>RSS feed of new Philadelphia legislative documents. Search through the documents at http://legislation.phila.gov/. Do even more with the data at http://scraperwiki.com/scrapers/philadelphia_legislative_files/.</description>'
print '    <link>http://scraperwiki.com/scrapers/%s/</link>' % sourcescraper
#print '    <lastBuildDate>%s</lastBuildDate>\n' % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <pubDate>%s</pubDate>'  % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print '    <atom:link href="http://scraperwikiviews.com/run/%s/" rel="self" type="application/rss+xml" />' % view

# rows
scraperwiki.sqlite.attach('philadelphia_legislative_files')
rows = scraperwiki.sqlite.select('* from `philadelphia_legislative_files`.swdata')

# Since I did not store the dates as datetime fields in the database, I have to 
# do it here.  This is not efficient, and in the long term dates should be stored
# in a reasonable format.
def row_date(row):
    date_str = row.get('intro_date')
    if '/' in date_str:
        return strptime(date_str, '%m/%d/%Y')
    elif 'T' in date_str:
        return strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    else:
        return strptime(date_str, '%Y-%m-%d')

rows = sorted(rows, reverse=True, key=row_date)

more_allowed  = 1000
for row in rows:
    if not more_allowed:
        break

    print '    <item>'
    print '      <title>%s</title>' % row.get('title')
    print '      <link>%s</link>' % escape(row.get('url'))
    print '      <guid>%s</guid>' % escape(row.get('url'))
    print '      <description>The %s introduced by %s is currently %s.</description>' % (row.get('type'), row.get('sponsors'), row.get('status'))
    print '      <pubDate>%s</pubDate>' %  strftime("%a, %d %b %Y %H:%M:%S +0000", row_date(row))
    print '    </item>'
    more_allowed -= 1

print ' </channel>'
print '</rss> '
