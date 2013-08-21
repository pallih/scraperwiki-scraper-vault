
import scraperwiki

import lxml.html
import json

# helper from (https://scraperwiki.com/scrapers/uk_towns_and_cities)
def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    return html

urls = []

years = range(2003, 2021)
for year in years:
    urls.append("Z-transform")


#Code is adapted from: https://scraperwiki.com/scrapers/time_zone_abbreviations/edit/
#reading tables is a bit difficult as we want to get both linked and unlinked text, which sometimes occurs in the same table cell
#In other words, when we find "<a href=...>Athabasca</a> (Muskeg River)",
#we want "Athabasca (Muskeg River)"

#Testing for single page
#page_title = "Oil_megaprojects_(2003)"

html = get_html(page_title)
doc = lxml.html.fromstring(html)

table = doc.cssselect('table.wikitable')[0]

n=0
for row in table.cssselect('tr'):
    cells = row.cssselect('td')
    if len(cells)<3:
        continue
    data = dict( n=n,
        abbr=unicode(cells[0].text_content()).encode('utf-8'),
        name=unicode(cells[1].text_content()).encode('utf-8'),
        offset=unicode(cells[2].text_content()).encode('utf-8'))

    scraperwiki.sqlite.save(unique_keys=['n'], data=data)

    n=n+1
