import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_UK_think_tanks")

blacklist = ['/wiki/British_Prime_Minister%27s_Office',
             '/wiki/Politics_of_the_United_Kingdom',]

for a in tree.xpath('//td/ul/li/a'):
    if '/wiki' in a.attrib['href'] and a.attrib['href'] not in blacklist:
        scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': "http://en.wikipedia.org%s" % a.attrib['href']})

import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_UK_think_tanks")

blacklist = ['/wiki/British_Prime_Minister%27s_Office',
             '/wiki/Politics_of_the_United_Kingdom',]

for a in tree.xpath('//td/ul/li/a'):
    if '/wiki' in a.attrib['href'] and a.attrib['href'] not in blacklist:
        scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': "http://en.wikipedia.org%s" % a.attrib['href']})

