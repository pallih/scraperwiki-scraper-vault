# Liverpool Schools Data

# Data from Dept for Education (released under Crown Copyright):
# http://www.education.gov.uk/schools/performance/download_data.html
# 
# Data used here in accordance with the DfE's terms:
# http://www.education.gov.uk/help/legalinformation/a005237/use-of-crown-copyright-material


import scraperwiki           
scraperwiki.scrape('http://ext.laegemiddelstyrelsen.dk/tilladelselaegertandlaeger/tilladelse_laeger_tandlaeger_full_soeg.asp?sort=Profession_&n=&v=')
print html

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'Profession' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data