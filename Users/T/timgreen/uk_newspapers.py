###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import lxml.html

# retrieve a page
tree = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_newspapers_in_the_United_Kingdom")

for tr in tree.xpath('//table[@class="sortable wikitable"]/tr'):
    tds = tr.xpath('td/a')

    if len(tds) != 0:
        scraperwiki.sqlite.save(['url'], {'name': tds[0].text, 'url': 'http://en.wikipedia.org%s' % tds[0].attrib['href']})
