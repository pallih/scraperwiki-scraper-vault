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

page_title = "ISO_3166-1"

html = get_html(page_title)
doc = lxml.html.fromstring(html)

for count, tr in enumerate(doc.cssselect('tr')):
    row = [(td.text_content()) for td in tr.cssselect('td')]
    if len(row)==5:
        for ahref in tr.cssselect('a'):
            detailink = ahref.attrib['href']
            if detailink.find(':',0,len(detailink)) != -1:
                detailink = detailink[6:]
                print detailink
        now = datetime.datetime.now()
        data ={"tmsp_scraped":str(now), "eng_short_name":row[0], "alpha_2_code":row[1], "alpha_3_code":row[2], "numeric_code":row[3], "iso_31662_code":detailink}
        scraperwiki.sqlite.save(unique_keys=["eng_short_name"], data=data, table_name="s_iso31661")
        
        html = get_html(detailink)
        doc = lxml.html.fromstring(html)

        for count, tr in enumerate(doc.cssselect('tr')):
            row = [td.text_content() for td in tr.cssselect('td')]
            row2 = [td.text_content() for td in tr.cssselect('td')]
            if len(row)>0:
                if row[0][:2] == detailink[11:]:
                    now = datetime.datetime.now()
                    data = {"tmsp_scraped":str(now), "iso_31662_code":detailink, "region_code":row[0], "region_desc":row[1], "region_desc_utf8":row2[1]}
                    scraperwiki.sqlite.save(unique_keys=["iso_31662_code","region_code"], data=data, table_name="s_iso31662_region")


        
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

page_title = "ISO_3166-1"

html = get_html(page_title)
doc = lxml.html.fromstring(html)

for count, tr in enumerate(doc.cssselect('tr')):
    row = [(td.text_content()) for td in tr.cssselect('td')]
    if len(row)==5:
        for ahref in tr.cssselect('a'):
            detailink = ahref.attrib['href']
            if detailink.find(':',0,len(detailink)) != -1:
                detailink = detailink[6:]
                print detailink
        now = datetime.datetime.now()
        data ={"tmsp_scraped":str(now), "eng_short_name":row[0], "alpha_2_code":row[1], "alpha_3_code":row[2], "numeric_code":row[3], "iso_31662_code":detailink}
        scraperwiki.sqlite.save(unique_keys=["eng_short_name"], data=data, table_name="s_iso31661")
        
        html = get_html(detailink)
        doc = lxml.html.fromstring(html)

        for count, tr in enumerate(doc.cssselect('tr')):
            row = [td.text_content() for td in tr.cssselect('td')]
            row2 = [td.text_content() for td in tr.cssselect('td')]
            if len(row)>0:
                if row[0][:2] == detailink[11:]:
                    now = datetime.datetime.now()
                    data = {"tmsp_scraped":str(now), "iso_31662_code":detailink, "region_code":row[0], "region_desc":row[1], "region_desc_utf8":row2[1]}
                    scraperwiki.sqlite.save(unique_keys=["iso_31662_code","region_code"], data=data, table_name="s_iso31662_region")


        
