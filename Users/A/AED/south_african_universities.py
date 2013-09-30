import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_universities_in_South_Africa")

for a in tree.xpath('//tr/td[1]/a'):
    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href'] })

import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_universities_in_South_Africa")

for a in tree.xpath('//tr/td[1]/a'):
    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href'] })

