import scraperwiki
import lxml.html
from datetime import datetime

url = "http://www.hertzfreerider.se/unauth/list_transport_offer.aspx"
html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)
for el in root.cssselect("span.offer_header"):
    row = el.text_content()
    now = datetime.now()
    print scraperwiki.sqlite.save(unique_keys=["when"], data={"when":now, "row":row})


