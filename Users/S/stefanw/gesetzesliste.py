import re

import scraperwiki


BASE_URL = 'http://www.gesetze-im-internet.de/Teilliste_%s.html'
CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'

# Evil parsing of HTML with regex'
REGEX = re.compile('href="\./([^\/]+)/index.html"><abbr title="([^"]*)">([^<]+)</abbr>')

laws = []

for char in CHARS:
    print "Loading part list %s" % char
    try:
        html = scraperwiki.scrape(BASE_URL % char.upper())
    except Exception:
        continue
    html = html.decode('iso-8859-1')
    matches = REGEX.findall(html)
    for match in matches:
        laws.append({
            'slug': match[0],
            'name': match[1].replace('&quot;', '"'),
            'abbreviation': match[2].strip()
        })
    
scraperwiki.sqlite.save(unique_keys=['slug'], data=laws)