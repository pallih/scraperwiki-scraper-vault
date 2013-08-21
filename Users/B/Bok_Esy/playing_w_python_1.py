import scraperwiki
import lxml.html
import re
import urllib2
import datetime

jUrl = "http://www.gov.im/ded/jobcentre/jobInfo.aspx?id="

def ScrapeW(number):
    url = "%s%05d" % (jUrl, number)
    root = lxml.html.parse(url).getroot()
    content = root.cssselect("div.JobCentreInformationPanel")
    assert len(content) == 1, url
    tables = content[0].cssselect("table")
#    assert 1 <= len(tables) <= 4, (url)
    html = lxml.html.tostring(root)
    out2 = re.search('Sorry, your bookmarked job is no longer available.', html)
    if out2:
        return None

    data = {"number":number, "url":url}
    data ["html"] = html

    scraperwiki.sqlite.save(unique_keys=["number", "html"], data=data, table_name="draft")

def mainSc():
    for i in range(67509, 1, -1):
        ScrapeW(i)
mainSc()