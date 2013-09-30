import scraperwiki
import lxml.html

base_url = "https://www.cia.gov/library/publications/the-world-factbook/"

html = scraperwiki.scrape(base_url+"docs/flagsoftheworld.html")
root = lxml.html.fromstring(html)

imgs = root.cssselect("img.flag_border")

for i in imgs:
    flag = base_url + i.attrib['src'].replace("../", "", 1)
    country = i.attrib['title'].replace("Flag of ", "", 1)
    record = {"country" : country, "flag" : flag}
    scraperwiki.sqlite.save(unique_keys=["country"], data=record)

import scraperwiki
import lxml.html

base_url = "https://www.cia.gov/library/publications/the-world-factbook/"

html = scraperwiki.scrape(base_url+"docs/flagsoftheworld.html")
root = lxml.html.fromstring(html)

imgs = root.cssselect("img.flag_border")

for i in imgs:
    flag = base_url + i.attrib['src'].replace("../", "", 1)
    country = i.attrib['title'].replace("Flag of ", "", 1)
    record = {"country" : country, "flag" : flag}
    scraperwiki.sqlite.save(unique_keys=["country"], data=record)

