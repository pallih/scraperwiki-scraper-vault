import scraperwiki
html = scraperwiki.scrape('http://www.ico.gov.uk/tools_and_resources/decision_notices.aspx')

import lxml.html
root = lxml.html.fromstring(html)
for option in root.cssselect("select#content_0_authority option"):
    name=option.text_content()
    scraperwiki.sqlite.save(unique_keys=["name"], data={"name": name})
import scraperwiki
html = scraperwiki.scrape('http://www.ico.gov.uk/tools_and_resources/decision_notices.aspx')

import lxml.html
root = lxml.html.fromstring(html)
for option in root.cssselect("select#content_0_authority option"):
    name=option.text_content()
    scraperwiki.sqlite.save(unique_keys=["name"], data={"name": name})
