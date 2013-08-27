import scraperwiki
import re
import scraperwiki
import lxml.html 

         
html = scraperwiki.scrape("http://www.myhospitals.gov.au/hospital/armidale-hospital/services/emergency-department")     
root = lxml.html.fromstring(html)

for percentage in root.cssselect("div.firstColumn"):
    print percentage.text_content().split(')')[1]
    import scraperwiki
import re
import scraperwiki
import lxml.html 

         
html = scraperwiki.scrape("http://www.myhospitals.gov.au/hospital/armidale-hospital/services/emergency-department")     
root = lxml.html.fromstring(html)

for percentage in root.cssselect("div.firstColumn"):
    print percentage.text_content().split(')')[1]
    import scraperwiki
import re
import scraperwiki
import lxml.html 

         
html = scraperwiki.scrape("http://www.myhospitals.gov.au/hospital/armidale-hospital/services/emergency-department")     
root = lxml.html.fromstring(html)

for percentage in root.cssselect("div.firstColumn"):
    print percentage.text_content().split(')')[1]
    