from datetime import datetime
import uuid
import scraperwiki           

sourcescraper = 'timeout'

atom_header_template = ('<?xml version="1.0" encoding="utf-8"?>'
    ' <feed xmlns="http://www.w3.org/2005/Atom"'
    ' xmlns:georss="http://www.georss.org/georss"'
    ' xmlns:gml="http://www.opengis.net/gml">'
    '<author>'
    '<name>John Donovan</name>'
    '</author>'
    '<id>{id}</id>'
    '<title>{title}</title>'
    '<updated>{updated}Z</updated>'
    '<link rel="self" href="http://geospark.co.uk/timeout-feed"/>'
    '<link href="http://geospark.co.uk/"/>')

atom_entry_template = ('<entry>'
    '<id>{id}</id>'
    '<title>{title}</title>'
    '<link href="{link}"/>'
    '<updated>{updated}Z</updated>'
    '<summary>{summary}</summary>'
    '<georss:point>{pos}</georss:point>'
    '</entry>')

atom_footer_template = '</feed>'

feed_uuid = '421842c6-ecea-5365-9a7b-44cc3973d802'

scraperwiki.utils.httpresponseheader('Content-Type', 'application/atom+xml')
scraperwiki.sqlite.attach(sourcescraper)

feed = {'id': 'urn:uuid:' + feed_uuid, 'title': 'TimeOut Art events in London', 'updated': datetime.now().isoformat('T')}
print(atom_header_template.format(**feed))


for event in scraperwiki.sqlite.select("* from swdata limit 1"):
    atom_entry = {'id': 'uri:' + event['link'],
                  'title': event['title'],
                  'link': 'http://geospark.co.uk/timeout-feed/' + str(event['id']),
                  'updated': event['pubDate'],
                  'summary': event['description'],
                  'pos': str(event['lat']) + ' '  + str(event['lon'])
                 }
    print(atom_entry_template.format(**atom_entry))

print(atom_footer_template)

# [{u'end': u'2013-04-28T00:00:00', u'description': u'It is an act of splendid cheekiness for a maritime museum to celebrate a photographer who barely crossed his own land, let alone the seas. Think of Ansel Adams and you think of imposing American mountainscapes and glowing, moon-backed clouds. Monumental...', u'pubDate': u'2013-03-23T22:03:51.368574', u'title': u'Ansel Adams: Photography from the Mountains to the Sea', u'lon': -0.003746383189667179, u'start': u'2013-03-24T00:00:00', u'link': u'http://www.timeout.com/london/popular-venues/ansel-adams-photography-from-the-mountains-to-the-sea', u'address': u'National Maritime Museum Park Row, Greenwich, SE10 9NF', u'lat': 51.48115383168784, u'image_url': u'http://media.timeout.com/images/resizeBestFit/135161/660/370/image.jpg', u'id': 228699, u'categories': u'art'}]

