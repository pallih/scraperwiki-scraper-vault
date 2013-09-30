import scraperwiki
from urllib import quote
from urlparse import urlparse

sourcescraper = 'uk-local-council-websites'

data = list(scraperwiki.datastore.getData(sourcescraper, limit=-1, offset=0))

print "<html><body>"
print "<h2>Total Councils: %s</h2>" % len(data)
print "<h2>Councils mentioning IAR: %s</h2>" % len([x for x in data if int(x.get('mentions_of_iar')) > 0])
print "<table><tr><th>Council</th><th>Website</th><th>Mentions of IAR</th></tr>"

def search_url(url):
    return 'http://www.google.co.uk/search?q=' + quote('"information asset register" inurl:%s' % urlparse(url).netloc)

for d in sorted(data, key=lambda x: x['council_name']):
    num_mentions = int(d.get('mentions_of_iar', 0))
    if num_mentions > 0:
        print "<tr><td>%s</td><td>%s</td><td><a href='%s' target='_blank'>%s</a></td></tr>" % (d['council_name'], d['url'], search_url(d['url']), num_mentions)
    else:
        print "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (d['council_name'], d['url'], num_mentions)

print "</table></body><html>"
import scraperwiki
from urllib import quote
from urlparse import urlparse

sourcescraper = 'uk-local-council-websites'

data = list(scraperwiki.datastore.getData(sourcescraper, limit=-1, offset=0))

print "<html><body>"
print "<h2>Total Councils: %s</h2>" % len(data)
print "<h2>Councils mentioning IAR: %s</h2>" % len([x for x in data if int(x.get('mentions_of_iar')) > 0])
print "<table><tr><th>Council</th><th>Website</th><th>Mentions of IAR</th></tr>"

def search_url(url):
    return 'http://www.google.co.uk/search?q=' + quote('"information asset register" inurl:%s' % urlparse(url).netloc)

for d in sorted(data, key=lambda x: x['council_name']):
    num_mentions = int(d.get('mentions_of_iar', 0))
    if num_mentions > 0:
        print "<tr><td>%s</td><td>%s</td><td><a href='%s' target='_blank'>%s</a></td></tr>" % (d['council_name'], d['url'], search_url(d['url']), num_mentions)
    else:
        print "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (d['council_name'], d['url'], num_mentions)

print "</table></body><html>"
