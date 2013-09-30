# Blank Python

import scraperwiki
import urlparse

base_url = "http://www.siac.tribunals.gov.uk/outcomes2007onwards.htm"

html = scraperwiki.scrape(base_url)

print html

import lxml.html
root = lxml.html.fromstring(html)

field_names = ["date", "appeal_no", "appellant", "appeal_type", "hearing_type", "hearing_date", "outcome", "leave"]

for tr in root.cssselect("table[class='siactable'] tbody tr"):
    tds = tr.cssselect("td")

    #Skip bogus row with no elements
    if len(tds) == 0:
        continue

    fields = [td.text_content() for td in tds]

    data = dict(zip(field_names, fields))

    # Fix appeal no field to give each hearing a unique id
    data["appeal_no"] = "%s (%s)" % (data["appeal_no"], data["hearing_type"]) 

    try:
        link = tds[6].cssselect("a")
        link_rel = link[0].get("href")
        link_abs = urlparse.urljoin(base_url, link_rel)
    except IndexError:
        print data
        link_abs = ""
    data["judgment_url"] = link_abs

    scraperwiki.sqlite.save(unique_keys=['appeal_no'], data=data)
    #print data

# Blank Python

import scraperwiki
import urlparse

base_url = "http://www.siac.tribunals.gov.uk/outcomes2007onwards.htm"

html = scraperwiki.scrape(base_url)

print html

import lxml.html
root = lxml.html.fromstring(html)

field_names = ["date", "appeal_no", "appellant", "appeal_type", "hearing_type", "hearing_date", "outcome", "leave"]

for tr in root.cssselect("table[class='siactable'] tbody tr"):
    tds = tr.cssselect("td")

    #Skip bogus row with no elements
    if len(tds) == 0:
        continue

    fields = [td.text_content() for td in tds]

    data = dict(zip(field_names, fields))

    # Fix appeal no field to give each hearing a unique id
    data["appeal_no"] = "%s (%s)" % (data["appeal_no"], data["hearing_type"]) 

    try:
        link = tds[6].cssselect("a")
        link_rel = link[0].get("href")
        link_abs = urlparse.urljoin(base_url, link_rel)
    except IndexError:
        print data
        link_abs = ""
    data["judgment_url"] = link_abs

    scraperwiki.sqlite.save(unique_keys=['appeal_no'], data=data)
    #print data

