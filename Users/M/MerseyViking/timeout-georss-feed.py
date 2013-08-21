from datetime import datetime
import dateutil.parser
import uuid
import scraperwiki

sourcescraper = 'timeout'

rss_header_template = ('<?xml version="1.0" encoding="utf-8"?>'
    ' <rss version="2.0"'
    ' xmlns:georss="http://www.georss.org/georss"'
    ' xmlns:gml="http://www.opengis.net/gml">'
    '<channel>'
    '<title>{title}</title>'
    '<description>A maps of art events in London as listed in TimeOut online magazine.</description>'
    '<link>http://geospark.co.uk/timeout-feed</link>'
    )

rss_entry_template = ('<item>'
    '<guid isPermaLink="true">{id}</guid>'
    '<title>{title}</title>'
    '<pubDate>{updated}</pubDate>'
    '<description>{summary}</description>'
    '<georss:where>'
    '<gml:Point>'
    '<gml:pos>{pos}</gml:pos>'
    '</gml:Point>'
    '</georss:where>'
    '</item>')

rss_footer_template = '</channel></rss>'

scraperwiki.utils.httpresponseheader('Content-Type', 'application/rss+xml')
scraperwiki.sqlite.attach(sourcescraper)

feed = {'title': 'TimeOut Art events in London'}
print(rss_header_template.format(**feed))

for event in scraperwiki.sqlite.select("* from swdata limit 1"):
    rfc822_date = dateutil.parser.parse(event['pubDate'] + 'Z').strftime('%a, %d %b %Y %H:%m:%S %z')

    rss_entry = {'id': event['link'],
                  'title': event['title'],
                  'updated': rfc822_date,
                  'summary': event['description'],
                  'pos': str(event['lat']) + ' '  + str(event['lon'])
                 }
    print(rss_entry_template.format(**rss_entry))

print(rss_footer_template)

# [{u'end': u'2013-04-28T00:00:00', u'description': u'It is an act of splendid cheekiness for a maritime museum to celebrate a photographer who barely crossed his own land, let alone the seas. Think of Ansel Adams and you think of imposing American mountainscapes and glowing, moon-backed clouds. Monumental...', u'pubDate': u'2013-03-23T22:03:51.368574', u'title': u'Ansel Adams: Photography from the Mountains to the Sea', u'lon': -0.003746383189667179, u'start': u'2013-03-24T00:00:00', u'link': u'http://www.timeout.com/london/popular-venues/ansel-adams-photography-from-the-mountains-to-the-sea', u'address': u'National Maritime Museum Park Row, Greenwich, SE10 9NF', u'lat': 51.48115383168784, u'image_url': u'http://media.timeout.com/images/resizeBestFit/135161/660/370/image.jpg', u'id': 228699, u'categories': u'art'}]

