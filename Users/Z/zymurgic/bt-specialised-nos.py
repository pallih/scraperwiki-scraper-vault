###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This tries to make sense of the rather complicated BT price list PDF
###########################################################################################

# Note. BT have made this difficult to scrape. Their PDF now links to HTML pricelist information 
# which is what we're actually after.
#
# Need to re-code this scraper to traverse all the hyperlinks in the PDF and scrape them (currently HTML) for the
# cns to chargeband mappings.

import scraperwiki
import json
import re
import lxml.html 
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.productsandservices.bt.com/consumer/consumerProducts/pdf/SpecialisedNos.pdf"
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
pat = re.compile("^[a-z]+?[0-9]*?$")
htmlpat = re.compile("\.htm#")
urls = set()
anchors = set(s.findAll('a'))
for a in anchors:
    a_attrs = dict(a.attrs)
    url=a_attrs[u'href']
    urls.add(url)
#    urls.add(url.replace('_boo/1','_boo/2-1'))
    urls.add(url.replace('_boo/','_boo/2-'))

def trawlhtml (url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr"): 
        tds = tr.cssselect("td") 
        if len(tds)>1:
            trimmed = tds[0].text_content().replace("(e)","").replace("(f)","").replace(" ","")
            trimmedcg = tds[1].text_content().replace(" ","")
            if (trimmed.isdigit() and len(trimmed)>3):
                data = { 
                    'cns' : trimmed, 
                    'cg' : trimmedcg
                }
                scraperwiki.sqlite.save (unique_keys=["cns"],data={"cns":trimmed,"cg":trimmedcg})

for url in urls:
    print url
    trawlhtml(url)

for t in s.findAll('text'):
    if (t.text != " ") and (t.text != "Code") and (t.text !='Type of Call') and (len(t.text)<13):
        trimmed = t.text.replace(" ","")
#        if trimmed.startswith("0") and trimmed.isdigit():
        if trimmed.isdigit() and (len(trimmed)>3):
         cns=trimmed
        elif ((cns) and (pat.match(trimmed))):
         print cns, trimmed
         data = {cns : trimmed}
         print data
         scraperwiki.sqlite.save (unique_keys=["cns"],data={"cns":cns,"cg":trimmed})
         cns=""
    
