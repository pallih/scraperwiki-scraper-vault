import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_sovereign_states")

for a in tree.xpath('//td/b/a'):
    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href']})

import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_sovereign_states")

for a in tree.xpath('//td/b/a'):
    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href']})

