# Blank Python
import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/Category:Industry_trade_groups_based_in_the_United_Kingdom")

for a in tree.xpath('//td/ul/li/a'):
    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': "http://www.wikipedia.org%s" % a.attrib['href']})
# Blank Python
import scraperwiki
import lxml.html

tree = lxml.html.parse("http://en.wikipedia.org/wiki/Category:Industry_trade_groups_based_in_the_United_Kingdom")

for a in tree.xpath('//td/ul/li/a'):
    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': "http://www.wikipedia.org%s" % a.attrib['href']})
