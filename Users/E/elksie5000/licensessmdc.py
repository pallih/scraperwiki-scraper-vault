import scraperwiki
import lxml.html

url = "https://licensing.staffsmoorlands.gov.uk/protected/wca/publicRegisterLicActPremisesLevel1.jsp"


html = scraperwiki.scrape(url)
print html
root = lxml.html.fromstring(html)

import scraperwiki
import lxml.html

url = "https://licensing.staffsmoorlands.gov.uk/protected/wca/publicRegisterLicActPremisesLevel1.jsp"


html = scraperwiki.scrape(url)
print html
root = lxml.html.fromstring(html)

