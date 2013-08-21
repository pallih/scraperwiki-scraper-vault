# Scraper to grab list of Pope names from wikipedia.
# The abbreviations are not unique.

import scraperwiki

import lxml.html
import json

# helper from (https://scraperwiki.com/scrapers/uk_towns_and_cities) & List_of_time zones and abbreviations
def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    return html

page_title = "List_of_popes"
#page title = "List_of_time_zone_abbreviations"

html = get_html(page_title)
doc = lxml.html.fromstring(html)


for n in range(0, 21):
    print n
    table = doc.cssselect('table.wikitable')[n]
    n=0
    for row in table.cssselect('tr'):
        cells = row.cssselect('td')
        #print len(cells)
        if len(cells)<7:
            continue
        data = dict( n=n,
            cell0=unicode(cells[0].text_content()).encode('utf-8'),
            cell1=unicode(cells[1].text_content()).encode('utf-8'),
            cell2=unicode(cells[2].text_content()).encode('utf-8'),
            cell3=unicode(cells[3].text_content()).encode('utf-8'),
            cell4=unicode(cells[4].text_content()).encode('utf-8'),
            cell5=unicode(cells[5].text_content()).encode('utf-8'),
            cell6=unicode(cells[6].text_content()).encode('utf-8'))

        scraperwiki.sqlite.save(unique_keys=['n'], data=data)
        n=n+1

