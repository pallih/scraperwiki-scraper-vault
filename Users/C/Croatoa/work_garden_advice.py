import scraperwiki
import lxml.html

errors = 0
i = 1
while errors < 50:
    html = scraperwiki.scrape('http://www.capitalgrowth.org/spaces/?id=%s' % i)
    dom = lxml.html.fromstring(html)
    if len(dom.cssselect('#orgdetails h2')):
            # valid property ID… let's scrape!
        print i, dom.cssselect('#orgdetails h2')[0].text_content()
errors = 0
    elif len( dom.cssselect('#orgdetails div')[-1].text_content()):
            # not a valid property ID… might be at the end
        print i, '-'
        errors += 1
    else:
        print 'oh dear! No garden details found, but no warning message either'
        break
    i += 1
