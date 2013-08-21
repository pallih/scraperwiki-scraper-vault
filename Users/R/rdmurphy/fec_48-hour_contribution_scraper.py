import scraperwiki
import requests
import lxml.html
import urllib
import json
import os, cgi

NYT_KEY = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))["NYT_KEY"]

BASE_URI = "http://api.nytimes.com/svc/elections/us/v3/finances/2012"

url_build = BASE_URI + "/committees/C00389197/filings.json?api-key=" + NYT_KEY
print url_build
html = scraperwiki.scrape(url_build)
print html
#filing_r = requests.get(url_build, params=API_KEY)
#print filing_r

#filing_response = json.loads(filing_r.text)
#returned_reports = filing_response["results"]

#for report in returned_reports:
    #if report["form_type"] == "F6":
    #    url = report["fec_uri"] + "f65"
    #    print url
    #    content = urllib.urlopen(url).read()
    #    doc = lxml.html.fromstring(content)
    #    names = doc.cssselect("h3")[1:][:-1]
    #    contributions = doc.cssselect("h4")
    #    name_contribs = zip(names, contributions)
    #    for entry in name_contribs:
    #        name = entry[0].text_content()
    #        date = entry[1].text_content()[19:][:10]
    #        amt = entry[1].text_content()[50:]
        
    #    print name, date, amt