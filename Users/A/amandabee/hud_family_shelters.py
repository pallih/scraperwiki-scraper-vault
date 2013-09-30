import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://www.hud.gov/local/ny/homeless/familiesshelters.cfm")
raw = lxml.html.fromstring(html)

for row in raw.cssselect("td#content-area p"):
    print row

    data = {
        'shelter':row.text_content()
#        'address':
#        'city':
#        'state':
#        'zip':
    }
    scraperwiki.sqlite.save(unique_keys=['shelter'], data=data)
import scraperwiki
import lxml.html 

html = scraperwiki.scrape("http://www.hud.gov/local/ny/homeless/familiesshelters.cfm")
raw = lxml.html.fromstring(html)

for row in raw.cssselect("td#content-area p"):
    print row

    data = {
        'shelter':row.text_content()
#        'address':
#        'city':
#        'state':
#        'zip':
    }
    scraperwiki.sqlite.save(unique_keys=['shelter'], data=data)
