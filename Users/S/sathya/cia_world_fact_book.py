"""
CIA world fact book
"""

import scraperwiki
import lxml.html

html = scraperwiki.scrape("https://www.cia.gov/library/publications/the-world-factbook/geos/xx.html")
root = lxml.html.fromstring(html)
countries = root.cssselect("select[id='countryCode'] > option")

for country in countries:
    print country.text
    countryId = country.attrib["value"]
    if countryId == "":
        print "none"
    else:
        countryURL = "https://www.cia.gov/library/publications/the-world-factbook/geos/" + countryId + ".html"
        html2 = scraperwiki.scrape(countryURL)
        root2 = lxml.html.fromstring(html2)
        c_info = root2.cssselect("table[class='CollapsiblePanelContent']")
        for info in c_info:    
            print info.text_content()