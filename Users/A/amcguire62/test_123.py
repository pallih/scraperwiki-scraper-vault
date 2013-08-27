import re
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect('td')
    data = { 'Country' : tds[0].text }
    for item in tds:
        text = item.text_content()
        if text:
            if re.match("[1-9][0-9][0-9][0-9]", text):
                continue
            elif re.match("[1-9][0-9]*", text):
                data['years_in_school'] = int(text)
    print data

    scraperwiki.sqlite.save(unique_keys=['Country'], data=data)
import re
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect('td')
    data = { 'Country' : tds[0].text }
    for item in tds:
        text = item.text_content()
        if text:
            if re.match("[1-9][0-9][0-9][0-9]", text):
                continue
            elif re.match("[1-9][0-9]*", text):
                data['years_in_school'] = int(text)
    print data

    scraperwiki.sqlite.save(unique_keys=['Country'], data=data)
