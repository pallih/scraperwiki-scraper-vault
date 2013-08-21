import scraperwiki

# Blank Python

html = scraperwiki.scrape("http://www.linkedin.com/jsearch?keywords=marketing&searchLocationType=I&countryCode=us")

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("<il>"):
    tds = tr.cssselect("</il>")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data
