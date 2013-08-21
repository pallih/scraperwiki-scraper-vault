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

page_title = "List_of_FIPS_country_codes#See_also"

html = get_html(page_title)
doc = lxml.html.fromstring(html)

for count, tr in enumerate(doc.cssselect('tr')):
    row = [(td.text_content()) for td in tr.cssselect('td')]
    if len(row)==2:
        now = datetime.datetime.now()
        data = {"tmsp_scraped":str(now), "fips_country_code":row[0].strip(), "fips_country_name":row[1].strip()}
        scraperwiki.sqlite.save(unique_keys=["fips_country_code"],data=data, table_name = "s_fips_country")

page_title = "List_of_FIPS_region_codes_(A–C)"

html = get_html(page_title)
doc = lxml.html.fromstring(html)

for count, tr in enumerate(doc.cssselect('tr')):
    row = [(td.text_content()) for td in tr.cssselect('td')]
    print row
    #if len(row)==2:
    #    now = datetime.datetime.now()
    #    data = {"tmsp_scraped":str(now), "fips_country_code":row[0].strip(), "fips_country_name":row[1].strip()}
    #    scraperwiki.sqlite.save(unique_keys=["fips_country_code"],data=data, table_name = "s_fips_country")


