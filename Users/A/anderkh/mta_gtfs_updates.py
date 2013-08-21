import scraperwiki
import lxml.html
import dateutil.parser

# Blank Python

url = "http://www.mta.info/developers/download.html"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for el in root.xpath('//a'):
    if (el.text == 'Metro-North Railroad -'):
        parent = el.getparent()
        parts = parent.text_content().split('Updated ')
        dateStr = parts[len(parts)-1]
        updateDate = dateutil.parser.parse(dateStr)
        data = {
            'name':'Metro-North Railroad',
            'update_date' : updateDate
        }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        print updateDate
        break








