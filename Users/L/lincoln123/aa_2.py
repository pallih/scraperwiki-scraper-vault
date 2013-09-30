import scraperwiki

from lxml import html

url = "http://xiaoyongzi.github.io/web/index.html"
doc_text = scraperwiki.scrape(url)
#print doc_text

doc = html.fromstring(doc_text)

print doc

for row in doc.cssselect("#main div div article div div h2"):
    link_in_header = row.cssselect("a").pop()
    event_title = link_in_header.text
#    print repr(event_title)

    
