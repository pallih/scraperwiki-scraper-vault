import scraperwiki
import lxml.html
import urllib
import datetime
import json
import string

from unidecode import unidecode

def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    return html

reccount = 0
alluppercase = string.ascii_uppercase
for x in xrange(0,26):
    page_title = "List_of_airports_by_IATA_code:_" + alluppercase[x]
    html = get_html(page_title)
    doc = lxml.html.fromstring(html)
    for count, tr in enumerate(doc.cssselect('tr')):
        row = [unicode(td.text_content()).encode('utf-8') for td in tr.cssselect('td')]
        if len(row)==4:
            reccount+=1
            now = datetime.datetime.now()
            data = {"record_id":reccount, "tmsp_scraped":str(now), "iata_code":row[0], "icao_code":row[1], "airport_name":row[2], "location_served":row[3]}
            scraperwiki.sqlite.save(unique_keys=["record_id"], data=data, table_name="s_airport")


