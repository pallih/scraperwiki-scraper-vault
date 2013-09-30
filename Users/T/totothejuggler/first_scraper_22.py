
import scraperwiki           
html = scraperwiki.scrape("http://scholar.google.com/citations?hl=en&user=D8lvl64AAAAJ&view_op=list_works&pagesize=100")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'title' : tds[0].text_content(),
            'citations' : tds[1].text_content(),
            'year' : tds[3].text_content()
             
        }
        print data

        