import scraperwiki           
import lxml.html
import urllib2
import dateutil.parser as parser

url = "http://www.mnd.uscourts.gov/ncs/open_cases_report.html"
html = urllib2.urlopen(url).read()
print "The HTML file is %d bytes" % len(html)
print html


import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)==7:

        casedate = tds[0].text_content() # @TODO parse to ISO 8601

        data = {
            'filing_date' : casedate,
            'time_reported' : tds[1].text_content(),
            'case_number' : tds[2].text_content(),
            'case_title' : tds[3].text_content(),
            'case_type' : tds[4].text_content(),
            'judge' : tds[5].text_content(),
            'magistrate' : tds[6].text_content()
        }
        if data['case_number'] != "Case #":
            scraperwiki.sqlite.save(unique_keys=['case_number'], data=data)

import scraperwiki           
import lxml.html
import urllib2
import dateutil.parser as parser

url = "http://www.mnd.uscourts.gov/ncs/open_cases_report.html"
html = urllib2.urlopen(url).read()
print "The HTML file is %d bytes" % len(html)
print html


import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)==7:

        casedate = tds[0].text_content() # @TODO parse to ISO 8601

        data = {
            'filing_date' : casedate,
            'time_reported' : tds[1].text_content(),
            'case_number' : tds[2].text_content(),
            'case_title' : tds[3].text_content(),
            'case_type' : tds[4].text_content(),
            'judge' : tds[5].text_content(),
            'magistrate' : tds[6].text_content()
        }
        if data['case_number'] != "Case #":
            scraperwiki.sqlite.save(unique_keys=['case_number'], data=data)

