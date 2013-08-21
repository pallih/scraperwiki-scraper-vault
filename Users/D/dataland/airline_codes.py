import scraperwiki
import lxml.html
import urllib
import datetime
import json

from unidecode import unidecode

def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    return html

page_title = "Airline_codes-All"

html = get_html(page_title)
doc = lxml.html.fromstring(html)

for count, tr in enumerate(doc.cssselect('tr')):
    row = [unicode(td.text_content()).encode('utf-8') for td in tr.cssselect('td')]
    if count>=4:
        now = datetime.datetime.now()
        data = {"count":count, "tmsp_scraped":str(now), "iata_code":row[0], "icao_code":row[1], "airline":row[2], "callsign":row[3], "country":row[4], "comments":row[5]}
        scraperwiki.sqlite.save(unique_keys=["count"], data=data, table_name="s_aircode")

        
