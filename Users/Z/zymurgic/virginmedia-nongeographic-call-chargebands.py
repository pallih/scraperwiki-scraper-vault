###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This tries to make sense of the rather complicated Virgin Media price list PDF
###########################################################################################

import scraperwiki
import json
import re
import lxml.html
from BeautifulSoup import BeautifulSoup

# VirginMedia is known to move the URL of their non-geographic charges leaflet around
#pdfurl = "http://allyours.virginmedia.com/pdf/uk_non-geographical_calls_a.pdf"
#pdfurl = "http://shop.virginmedia.com/content/dam/allyours/pdf/005300_010511_Non%20geo_V1.pdf"
#pdfurl = "http://shop.virginmedia.com/content/dam/allyours/pdf/010911_Non%20geo_V1.pdf"
pdfurl = "http://shop.virginmedia.com/content/dam/allyours/pdf/011111_Non%20Geo_V1.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))
print s
name = None
all = []
data = {}
state = None
cns = None
trimmed = None
l = []
pat = re.compile("^[A-Z]+?[0-9]*?$")
htmlpat = re.compile("\.htm#")
urls = set()
anchors = set(s.findAll('a'))
for a in anchors:
    a_attrs = dict(a.attrs)
    url=a_attrs[u'href']
    urls.add(url)
    urls.add(url.replace('_boo/1','_boo/2-1'))

for url in urls:
    print url
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td")
        if len(tds)>1:
            trimmed = tds[0].text_content().replace(" ","")
            trimmedcg = tds[1].text_content().replace(" ","")
            if (trimmed.isdigit() and len(trimmed)>3):
                data = {
                    'cns' : trimmed,
                    'cg' : trimmedcg
                }
                scraperwiki.sqlite.save (unique_keys=["cns"],data={"cns":trimmed,"cg":trimmedcg})

for t in s.findAll('text'):
    if (t.text != " ") and (t.text != "Code") and (t.text !='Type of Call') and (len(t.text)<13):
        trimmed = t.text.replace(" ","")
#        if trimmed.startswith("0") and trimmed.isdigit():
        if trimmed.isdigit() and (len(trimmed)>3):
         cns=trimmed
        elif ((cns) and (pat.match(trimmed))):
#         print cns, trimmed
         data = {cns : trimmed}
#         print data
         scraperwiki.sqlite.save (unique_keys=["cns"],data={"cns":cns,"cg":trimmed})
         cns=""

###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This tries to make sense of the rather complicated Virgin Media price list PDF
###########################################################################################

import scraperwiki
import json
import re
import lxml.html
from BeautifulSoup import BeautifulSoup

# VirginMedia is known to move the URL of their non-geographic charges leaflet around
#pdfurl = "http://allyours.virginmedia.com/pdf/uk_non-geographical_calls_a.pdf"
#pdfurl = "http://shop.virginmedia.com/content/dam/allyours/pdf/005300_010511_Non%20geo_V1.pdf"
#pdfurl = "http://shop.virginmedia.com/content/dam/allyours/pdf/010911_Non%20geo_V1.pdf"
pdfurl = "http://shop.virginmedia.com/content/dam/allyours/pdf/011111_Non%20Geo_V1.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))
print s
name = None
all = []
data = {}
state = None
cns = None
trimmed = None
l = []
pat = re.compile("^[A-Z]+?[0-9]*?$")
htmlpat = re.compile("\.htm#")
urls = set()
anchors = set(s.findAll('a'))
for a in anchors:
    a_attrs = dict(a.attrs)
    url=a_attrs[u'href']
    urls.add(url)
    urls.add(url.replace('_boo/1','_boo/2-1'))

for url in urls:
    print url
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td")
        if len(tds)>1:
            trimmed = tds[0].text_content().replace(" ","")
            trimmedcg = tds[1].text_content().replace(" ","")
            if (trimmed.isdigit() and len(trimmed)>3):
                data = {
                    'cns' : trimmed,
                    'cg' : trimmedcg
                }
                scraperwiki.sqlite.save (unique_keys=["cns"],data={"cns":trimmed,"cg":trimmedcg})

for t in s.findAll('text'):
    if (t.text != " ") and (t.text != "Code") and (t.text !='Type of Call') and (len(t.text)<13):
        trimmed = t.text.replace(" ","")
#        if trimmed.startswith("0") and trimmed.isdigit():
        if trimmed.isdigit() and (len(trimmed)>3):
         cns=trimmed
        elif ((cns) and (pat.match(trimmed))):
#         print cns, trimmed
         data = {cns : trimmed}
#         print data
         scraperwiki.sqlite.save (unique_keys=["cns"],data={"cns":cns,"cg":trimmed})
         cns=""

