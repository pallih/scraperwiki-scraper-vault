import scraperwiki

from urllib2 import urlopen
from lxml.html import fromstring, tostring
import json
import dateutil.parser

from scraperwiki.sqlite import save, execute

raw = urlopen('http://www.foopee.com/punk/the-list/').read()
html = fromstring(raw)

for anchor in html.cssselect('dd a'):

    href = anchor.attrib['href']
    text = anchor.text_content()

    if not href.startswith('by-band'):
        continue

    data = {
        'band': text,
        'href': 'http://www.foopee.com/punk/the-list/' + href
    }
    save([], data)import scraperwiki

from urllib2 import urlopen
from lxml.html import fromstring, tostring
import json
import dateutil.parser

from scraperwiki.sqlite import save, execute

raw = urlopen('http://www.foopee.com/punk/the-list/').read()
html = fromstring(raw)

for anchor in html.cssselect('dd a'):

    href = anchor.attrib['href']
    text = anchor.text_content()

    if not href.startswith('by-band'):
        continue

    data = {
        'band': text,
        'href': 'http://www.foopee.com/punk/the-list/' + href
    }
    save([], data)