#Call scraperwiki libraries to analyse html code
import scraperwiki
import urlparse
from lxml import html

url="http://www-news.iaea.org/EventList.aspx"


doc_text=scraperwiki.scrape(url)
doc=html.fromstring(doc_text)

for row in doc.cssselect("#tblEvents tr"):
 link_in_header=row.cssselect("span.float-right-margin").pop()
 event_title=link_in_header.text
 print event_title