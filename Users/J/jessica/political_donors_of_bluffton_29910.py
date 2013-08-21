import scraperwiki

# Blank Python
import scraperwiki
params ={
     'state': 'SC',
     'zip' : '29910'
}
html = scraperwiki.scrape("http://query.nictusa.com/cgi-bin/qind/", params)
print html
import lxml.html
root = lxml.html.fromstring(html)
for table in root.cssselect("tr"):
    rows = tr.cssselect("td b")
    data = {
      'contributor' : rows[0].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=["contributor","recipient"], data=data)

