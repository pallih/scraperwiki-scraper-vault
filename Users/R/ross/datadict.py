import string
import scraperwiki
from lxml.html import fromstring

root = 'http://www.datadictionary.nhs.uk/items_index_{l}_child.asp'


for l in string.ascii_uppercase + '0':
    u = root.format(l=l)
    page = scraperwiki.scrape(u)
    items = []

    dom = fromstring(page)
    rows = dom.cssselect('table tr')[1:]
    for row in rows:
        items.append({'item':row[0].text_content()})

    scraperwiki.sqlite.save(['item'], items, 'datadict')import string
import scraperwiki
from lxml.html import fromstring

root = 'http://www.datadictionary.nhs.uk/items_index_{l}_child.asp'


for l in string.ascii_uppercase + '0':
    u = root.format(l=l)
    page = scraperwiki.scrape(u)
    items = []

    dom = fromstring(page)
    rows = dom.cssselect('table tr')[1:]
    for row in rows:
        items.append({'item':row[0].text_content()})

    scraperwiki.sqlite.save(['item'], items, 'datadict')import string
import scraperwiki
from lxml.html import fromstring

root = 'http://www.datadictionary.nhs.uk/items_index_{l}_child.asp'


for l in string.ascii_uppercase + '0':
    u = root.format(l=l)
    page = scraperwiki.scrape(u)
    items = []

    dom = fromstring(page)
    rows = dom.cssselect('table tr')[1:]
    for row in rows:
        items.append({'item':row[0].text_content()})

    scraperwiki.sqlite.save(['item'], items, 'datadict')