# Blank Python

import scraperwiki
import lxml.html
import urllib2

base_url = "http://www.europarl.europa.eu/members/archive/alphaOrder.do?letter=%s&language=EN"

for c in [chr(x) for x in range(65, 91)]:
    url = base_url % c

    print url
    response = urllib2.urlopen(url)
    tree = lxml.html.parse(response, base_url=url)

    for a in tree.xpath('//td[@class="listcontentdark_left"]/a'):
        #last, first = a.text.split(',')
        #last = last.capitalize().strip()
        #first = first.strip()
        
        scraperwiki.sqlite.save(unique_keys=['url'], data={'name': a.text.strip(), 'url': "http://www.europarl.europa.eu%s" % a.attrib['href']}, table_name='meps')

# Blank Python

import scraperwiki
import lxml.html
import urllib2

base_url = "http://www.europarl.europa.eu/members/archive/alphaOrder.do?letter=%s&language=EN"

for c in [chr(x) for x in range(65, 91)]:
    url = base_url % c

    print url
    response = urllib2.urlopen(url)
    tree = lxml.html.parse(response, base_url=url)

    for a in tree.xpath('//td[@class="listcontentdark_left"]/a'):
        #last, first = a.text.split(',')
        #last = last.capitalize().strip()
        #first = first.strip()
        
        scraperwiki.sqlite.save(unique_keys=['url'], data={'name': a.text.strip(), 'url': "http://www.europarl.europa.eu%s" % a.attrib['href']}, table_name='meps')

