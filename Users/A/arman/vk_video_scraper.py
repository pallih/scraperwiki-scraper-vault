import scraperwiki
import lxml.html as HTML
from urlparse import urlparse, parse_qs
import json as JSON
import urllib
query = 'select * from %s limit %s' % ('`anidub.videos`','3')
#query = urllib.quote_plus('select * from `anidub.videos` limit 10')
print query
json = scraperwiki.scrape('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=anidub&query=' + urllib.quote_plus(query))
objects = JSON.loads(json)
print objects
for obj in objects:
    player = scraperwiki.scrape(obj['link'])
    doc = HTML.fromstring(player)
    flashvars = doc.cssselect('embed')[0].get('flashvars')
    player_data = parse_qs('/?' + flashvars)
    links = []
    for k,v in player_data.iteritems():
        if k in ('url360', 'url480','url720'):
            links.append(v[0])

    print links
    print player_data['thumb']
    


import scraperwiki
import lxml.html as HTML
from urlparse import urlparse, parse_qs
import json as JSON
import urllib
query = 'select * from %s limit %s' % ('`anidub.videos`','3')
#query = urllib.quote_plus('select * from `anidub.videos` limit 10')
print query
json = scraperwiki.scrape('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=anidub&query=' + urllib.quote_plus(query))
objects = JSON.loads(json)
print objects
for obj in objects:
    player = scraperwiki.scrape(obj['link'])
    doc = HTML.fromstring(player)
    flashvars = doc.cssselect('embed')[0].get('flashvars')
    player_data = parse_qs('/?' + flashvars)
    links = []
    for k,v in player_data.iteritems():
        if k in ('url360', 'url480','url720'):
            links.append(v[0])

    print links
    print player_data['thumb']
    


import scraperwiki
import lxml.html as HTML
from urlparse import urlparse, parse_qs
import json as JSON
import urllib
query = 'select * from %s limit %s' % ('`anidub.videos`','3')
#query = urllib.quote_plus('select * from `anidub.videos` limit 10')
print query
json = scraperwiki.scrape('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=anidub&query=' + urllib.quote_plus(query))
objects = JSON.loads(json)
print objects
for obj in objects:
    player = scraperwiki.scrape(obj['link'])
    doc = HTML.fromstring(player)
    flashvars = doc.cssselect('embed')[0].get('flashvars')
    player_data = parse_qs('/?' + flashvars)
    links = []
    for k,v in player_data.iteritems():
        if k in ('url360', 'url480','url720'):
            links.append(v[0])

    print links
    print player_data['thumb']
    


import scraperwiki
import lxml.html as HTML
from urlparse import urlparse, parse_qs
import json as JSON
import urllib
query = 'select * from %s limit %s' % ('`anidub.videos`','3')
#query = urllib.quote_plus('select * from `anidub.videos` limit 10')
print query
json = scraperwiki.scrape('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=anidub&query=' + urllib.quote_plus(query))
objects = JSON.loads(json)
print objects
for obj in objects:
    player = scraperwiki.scrape(obj['link'])
    doc = HTML.fromstring(player)
    flashvars = doc.cssselect('embed')[0].get('flashvars')
    player_data = parse_qs('/?' + flashvars)
    links = []
    for k,v in player_data.iteritems():
        if k in ('url360', 'url480','url720'):
            links.append(v[0])

    print links
    print player_data['thumb']
    


