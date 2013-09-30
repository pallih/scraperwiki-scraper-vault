"""
Provide a description here, please.
"""

import scraperwiki
import lxml.html

URL = "http://unstats.un.org/unsd/demographic/products/socind/childbearing.htm"

html = scraperwiki.scrape(URL)
print html

root = lxml.html.fromstring(html)

# lxml doesn't like @ in your cssselect queries
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")

    country = tds[0].text_content()

    # Check the footnotes "..." means "Not available".
    try:
        life_expectancy = int(tds[4].text_content())
    except UnicodeEncodeError:
        life_expectancy = "-"

    data = {
        "country": country,
        "life_expectancy": life_expectancy
    }
    
    # Only print when debugging the script
    # print data

    scraperwiki.sqlite.save(unique_keys=["country"], data=data)

print "Done!""""
Provide a description here, please.
"""

import scraperwiki
import lxml.html

URL = "http://unstats.un.org/unsd/demographic/products/socind/childbearing.htm"

html = scraperwiki.scrape(URL)
print html

root = lxml.html.fromstring(html)

# lxml doesn't like @ in your cssselect queries
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")

    country = tds[0].text_content()

    # Check the footnotes "..." means "Not available".
    try:
        life_expectancy = int(tds[4].text_content())
    except UnicodeEncodeError:
        life_expectancy = "-"

    data = {
        "country": country,
        "life_expectancy": life_expectancy
    }
    
    # Only print when debugging the script
    # print data

    scraperwiki.sqlite.save(unique_keys=["country"], data=data)

print "Done!"