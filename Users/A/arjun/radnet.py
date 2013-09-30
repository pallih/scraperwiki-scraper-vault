import scraperwiki           
html = scraperwiki.scrape("http://radnet.com/doc_state_map.php?state=NY")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table"):
    tds = tr.cssselect("td")
    print tds
    for td in tds:
        if len(td)==12:
            data = {
                'doctor_name' : td[0].text_content()
            }
            print data

