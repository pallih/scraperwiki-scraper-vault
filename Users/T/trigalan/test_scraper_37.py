import scraperwiki           
html = scraperwiki.scrape("http://www.bbc.co.uk/sport/football/results")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'Man Utd' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data



import scraperwiki           
html = scraperwiki.scrape("http://www.bbc.co.uk/sport/football/results")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'Man Utd' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data



