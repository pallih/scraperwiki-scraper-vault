print "Hello, coding in the cloud!"

import scraperwiki
html = scraperwiki.scrape("http://www.saa.gov.uk/search.php?SEARCHED=1&SEARCH_TERM=ab10+1xy&DISPLAY_COUNT=100#results")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("*"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data

#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
