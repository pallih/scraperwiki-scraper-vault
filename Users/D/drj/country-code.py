#!/usr/bin/env python
# David Jones, Climate Code Foundation
# and Thomas Levine

# Scrape the CIA country code converter at:
url = "https://www.cia.gov/library/publications/the-world-factbook/appendix/appendix-d.html"

import urllib
import html5lib
from scraperwiki.sqlite import save

src = urllib.urlopen(url)

# From http://garethrees.org/2009/10/09/feed/
# Parse SRC as HTML.
tree_builder = html5lib.treebuilders.getTreeBuilder('dom')
parser = html5lib.html5parser.HTMLParser(tree = tree_builder)
dom = parser.parse(src)

# For serialisation
tree_walker = html5lib.treewalkers.getTreeWalker('dom')
html_serializer = html5lib.serializer.htmlserializer.HTMLSerializer()

#Get the keys
keys = []
# drj 2012-10-01.  huh.  CIA changed theit HTML and I can't get the
# html5lib API for getting element by class.  Probably better to rewrite
# using lxml and CSS selectors.
for th in dom.getElementsByClassName('smalltext'):
    key=th.getElementsByTagName('b')[0].firstChild.nodeValue
    if key in keys:
        break
    else:
        keys.append(key)
print keys
keys[2]='ISO_3166_twoletter'
keys.insert(3,'ISO_3166_threeletter')
keys.insert(4,'ISO_3166_number')

print keys

rows = []
for e in dom.getElementsByTagName('a'):
    h = e.getAttribute('href')
    if '/geos/' in h:
        # Should be a TR
        tr = e.parentNode.parentNode
        # This TR contains a bunch of TDs which variously contain the
        # codes for the country.
        # The acumulated result, for the row.
        row = []
    
        for td in tr.getElementsByTagName('td'):
            if not row:
                # first TD.  Has an A child, that contains the US
                # English country name.
                row.append(td.getElementsByTagName('a')[0].firstChild.nodeValue)
            else:
                row.append(td.firstChild.nodeValue)
    
        assert row[2] is None
        del row[2]
        print row
        d = dict(zip(keys, row))
        rows.append(d)
save(['Internet', 'FIPS 10', 'ISO_3166_twoletter'],rows,'country_codes')#!/usr/bin/env python
# David Jones, Climate Code Foundation
# and Thomas Levine

# Scrape the CIA country code converter at:
url = "https://www.cia.gov/library/publications/the-world-factbook/appendix/appendix-d.html"

import urllib
import html5lib
from scraperwiki.sqlite import save

src = urllib.urlopen(url)

# From http://garethrees.org/2009/10/09/feed/
# Parse SRC as HTML.
tree_builder = html5lib.treebuilders.getTreeBuilder('dom')
parser = html5lib.html5parser.HTMLParser(tree = tree_builder)
dom = parser.parse(src)

# For serialisation
tree_walker = html5lib.treewalkers.getTreeWalker('dom')
html_serializer = html5lib.serializer.htmlserializer.HTMLSerializer()

#Get the keys
keys = []
# drj 2012-10-01.  huh.  CIA changed theit HTML and I can't get the
# html5lib API for getting element by class.  Probably better to rewrite
# using lxml and CSS selectors.
for th in dom.getElementsByClassName('smalltext'):
    key=th.getElementsByTagName('b')[0].firstChild.nodeValue
    if key in keys:
        break
    else:
        keys.append(key)
print keys
keys[2]='ISO_3166_twoletter'
keys.insert(3,'ISO_3166_threeletter')
keys.insert(4,'ISO_3166_number')

print keys

rows = []
for e in dom.getElementsByTagName('a'):
    h = e.getAttribute('href')
    if '/geos/' in h:
        # Should be a TR
        tr = e.parentNode.parentNode
        # This TR contains a bunch of TDs which variously contain the
        # codes for the country.
        # The acumulated result, for the row.
        row = []
    
        for td in tr.getElementsByTagName('td'):
            if not row:
                # first TD.  Has an A child, that contains the US
                # English country name.
                row.append(td.getElementsByTagName('a')[0].firstChild.nodeValue)
            else:
                row.append(td.firstChild.nodeValue)
    
        assert row[2] is None
        del row[2]
        print row
        d = dict(zip(keys, row))
        rows.append(d)
save(['Internet', 'FIPS 10', 'ISO_3166_twoletter'],rows,'country_codes')