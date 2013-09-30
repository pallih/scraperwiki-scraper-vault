import re

import scraperwiki
import simplejson


BASE_URL = 'http://www.gesetze-im-internet.de/Teilliste_%s.html'
CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'

# Evil parsing of HTML with regex'
REGEX = re.compile('href="\./([^\/]+)/index.html">')

laws = []

for char in CHARS:
    print "Loading part list %s" % char
    try:
        html = scraperwiki.scrape(BASE_URL % char.upper())
    except Exception:
        continue
    ##result_json = simplejson.loads(html)
    ##for result_a in html['a']:
    
    html = html.decode('iso-8859-1')
    matches = REGEX.findall(html)
    ##matches = html.findall('a')
    for match in matches:
        url = "http://www.gesetze-im-internet.de/"+match+"/xml.zip"
        scraperwiki.sqlite.save(unique_keys=['url'], data={"url": url})
        ##laws.append({
        ##    'slug': match[0],
        ##    'name': match[1].replace('&quot;', '"'),
        ##    'abbreviation': match[2].strip()
        ##})import re

import scraperwiki
import simplejson


BASE_URL = 'http://www.gesetze-im-internet.de/Teilliste_%s.html'
CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'

# Evil parsing of HTML with regex'
REGEX = re.compile('href="\./([^\/]+)/index.html">')

laws = []

for char in CHARS:
    print "Loading part list %s" % char
    try:
        html = scraperwiki.scrape(BASE_URL % char.upper())
    except Exception:
        continue
    ##result_json = simplejson.loads(html)
    ##for result_a in html['a']:
    
    html = html.decode('iso-8859-1')
    matches = REGEX.findall(html)
    ##matches = html.findall('a')
    for match in matches:
        url = "http://www.gesetze-im-internet.de/"+match+"/xml.zip"
        scraperwiki.sqlite.save(unique_keys=['url'], data={"url": url})
        ##laws.append({
        ##    'slug': match[0],
        ##    'name': match[1].replace('&quot;', '"'),
        ##    'abbreviation': match[2].strip()
        ##})import re

import scraperwiki
import simplejson


BASE_URL = 'http://www.gesetze-im-internet.de/Teilliste_%s.html'
CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'

# Evil parsing of HTML with regex'
REGEX = re.compile('href="\./([^\/]+)/index.html">')

laws = []

for char in CHARS:
    print "Loading part list %s" % char
    try:
        html = scraperwiki.scrape(BASE_URL % char.upper())
    except Exception:
        continue
    ##result_json = simplejson.loads(html)
    ##for result_a in html['a']:
    
    html = html.decode('iso-8859-1')
    matches = REGEX.findall(html)
    ##matches = html.findall('a')
    for match in matches:
        url = "http://www.gesetze-im-internet.de/"+match+"/xml.zip"
        scraperwiki.sqlite.save(unique_keys=['url'], data={"url": url})
        ##laws.append({
        ##    'slug': match[0],
        ##    'name': match[1].replace('&quot;', '"'),
        ##    'abbreviation': match[2].strip()
        ##})