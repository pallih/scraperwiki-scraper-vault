import scraperwiki
from lxml import html

url = "https://twitter.com/Jasoninthehouse"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for row in doc.cssselect("#idtimeline"):
    link_in_header = row.cssselect("stream profile-stream").pop()
    event_title = link_in_header.text
    print timeline