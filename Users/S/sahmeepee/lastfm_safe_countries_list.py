#The shorter list of countries on Last.fm from the charts page

#All the world's countries are available in their database, but not as a published list/api
# and this is the only list available without a login. Can't find an identical match to their
# full country list elsewhere on the web.

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.last.fm/charts")
#print html

root = lxml.html.fromstring(html)
for option in root.xpath('//*[@id="selectachain-field-placea"]/option'):
        options = option.cssselect("option")
        data = {
            'country' : options[0].text_content().strip(),
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)#The shorter list of countries on Last.fm from the charts page

#All the world's countries are available in their database, but not as a published list/api
# and this is the only list available without a login. Can't find an identical match to their
# full country list elsewhere on the web.

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.last.fm/charts")
#print html

root = lxml.html.fromstring(html)
for option in root.xpath('//*[@id="selectachain-field-placea"]/option'):
        options = option.cssselect("option")
        data = {
            'country' : options[0].text_content().strip(),
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)